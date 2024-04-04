import asyncio
import logging
import os.path
from typing import Any, Union

import reactivex
import tornado.escape
import tornado.options
import tornado.web
import tornado.websocket
from reactivex import operators as ops, Subject, Observable
from reactivex.abc import DisposableBase
from reactivex.scheduler.eventloop import AsyncIOScheduler
from reactivex.subject import ReplaySubject
from tornado.options import define

from app import price_processor, avg_price_processor, trade_processor, trade_saver_processor
from app.mappers import Message, Trade
from app.tracking_client import connect

define("port", default=8080, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        inbound_msg = Subject()  # through this subject clients may send tick size configuration changes
        outbound_msg = ReplaySubject(20)  # cache 20 last messages
        handlers = [(r"/", MainHandler),
                    (r"/stream", StreamSocketHandler, {'inbound_msg': inbound_msg, 'outbound_msg': outbound_msg})]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "ui"),
            static_path=os.path.join(os.path.dirname(__file__), "ui"),
            xsrf_cookies=True,
        )
        super().__init__(handlers, **settings)

        loop = asyncio.get_running_loop()

        def price_processing_flow(source_of_msg: Observable[dict[str, Union[str, float]]]) -> Observable[Message]:
            return source_of_msg.pipe(
                price_processor.process,
                ops.share(),  # enable multiple subscriber to consume the same processed prices stream
                lambda source_of_prices: reactivex.merge(source_of_prices,
                                                         avg_price_processor.process(source_of_prices,
                                                                                     inbound_msg))
            )

        def trade_processing_flow(source_of_msg: Observable[dict[str, Union[str, float]]]) -> Observable[Message]:
            return source_of_msg.pipe(
                trade_processor.process,
                ops.share(),
                lambda source_of_prices: reactivex.merge(source_of_prices,
                                                         trade_saver_processor.save(source_of_prices))
            )

        (connect(loop)
         .pipe(
            ops.retry(),  # reconnect on client connection failure
            ops.share(),  # enable multiple subscriber to consume the same client connection
            lambda source_of_msg: reactivex.merge(
                price_processing_flow(source_of_msg),
                trade_processing_flow(source_of_msg)),
            ops.observe_on(AsyncIOScheduler(loop=loop)),
            ops.do_action(on_next=print, on_error=print))
         .subscribe(outbound_msg))


class MainHandler(tornado.web.RequestHandler):

    def check_origin(self, origin: str) -> bool:
        return False

    def get(self):
        self.render("index.html")


class StreamSocketHandler(tornado.websocket.WebSocketHandler):
    subscription: DisposableBase
    inbound_msg: Subject[int]
    outbound_msg: Subject[Message[Any]]

    def initialize(self, inbound_msg: Subject[int], outbound_msg: Subject[Message[Any]]):
        self.inbound_msg = inbound_msg
        self.outbound_msg = outbound_msg

    def check_origin(self, origin: str) -> bool:
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        self.subscription = self.outbound_msg.subscribe(on_next=lambda msg: self.send_updates(msg))

    def on_close(self):
        self.subscription.dispose()

    def send_updates(self, msg: Message[Any]):
        try:
            self.write_message({
                'timestamp': msg.timestamp,
                'data': {'price': msg.data.price, 'amount': msg.data.amount} if isinstance(msg.data,
                                                                                           Trade) else msg.data,
                'currency': msg.currency,
                'market': msg.market,
                'type': msg.type.name}, binary=False)
        except:
            logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        self.inbound_msg.on_next(int(message))


async def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8080)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
