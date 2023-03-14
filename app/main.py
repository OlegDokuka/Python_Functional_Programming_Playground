import asyncio
import logging
import os.path
from typing import Any, Union

import reactivex
import socketio  # type: ignore
import tornado.escape
import tornado.options
import tornado.web
import tornado.websocket
from reactivex import operators as ops, Subject, Observable
from reactivex.scheduler.eventloop import AsyncIOScheduler
from reactivex.subject import AsyncSubject, BehaviorSubject
from tornado.options import define

from app import price_processor, avg_price_processor, trade_processor, trade_saver_processor
from app.mappers import Message, Trade
from app.tracking_client import connect

define("port", default=8080, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        StreamSocketHandler.messages_sub = Subject()
        handlers = [(r"/", MainHandler), (r"/stream", StreamSocketHandler)]
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
                ops.share(),
                lambda source_of_prices: reactivex.merge(source_of_prices,
                                                         avg_price_processor.process(source_of_prices,
                                                                                     StreamSocketHandler.messages_sub))
            )

        def trade_processing_flow(source_of_msg: Observable[dict[str, Union[str, float]]]) -> Observable[Message]:
            return source_of_msg.pipe(
                trade_processor.process,
                ops.share(),
                lambda source_of_prices: reactivex.merge(source_of_prices,
                                                         trade_saver_processor.save(source_of_prices))
            )

        disposable = (connect(loop)
                      .pipe(ops.retry(),
                            ops.share(),
                            lambda source_of_msg: reactivex.merge(
                                price_processing_flow(source_of_msg),
                                trade_processing_flow(source_of_msg)),
                            ops.observe_on(AsyncIOScheduler(loop=loop)))
                      .subscribe(on_next=StreamSocketHandler.send_updates))


class MainHandler(tornado.web.RequestHandler):

    def check_origin(self, origin: str) -> bool:
        return False

    def get(self):
        self.render("index.html", messages=StreamSocketHandler.cache)


class StreamSocketHandler(tornado.websocket.WebSocketHandler):
    waiters: set[Any] = set()
    cache: list[Any] = []
    cache_size = 200

    def check_origin(self, origin: str) -> bool:
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        StreamSocketHandler.waiters.add(self)

    def on_close(self):
        StreamSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, msg: Message):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message({
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
        StreamSocketHandler.messages_sub.on_next(int(message))
        # parsed = tornado.escape.json_decode(message)
        # chat = {"id": str(uuid.uuid4()), "body": parsed["body"]}
        # chat["html"] = tornado.escape.to_basestring(
        #     self.render_string("message.html", message=chat)
        # )
        #
        # ChatSocketHandler.update_cache(chat)
        # ChatSocketHandler.send_updates(chat)


async def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8080)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

# async def main():
#     disposable = (connect(asyncio.get_running_loop())
#                   .pipe(price_processor.process,
#                         ops.do_action(on_next=print))
#                   .subscribe())
#
#     await asyncio.sleep(5)
#
#     disposable.dispose()
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#
#     # Schedule a call to hello_world()
#     loop.create_task(main())
#
#     # Blocking call interrupted by loop.stop()
#     try:
#         loop.run_forever()
#     finally:
#         loop.close()
