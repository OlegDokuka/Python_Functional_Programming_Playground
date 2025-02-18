import asyncio
import logging
from asyncio import AbstractEventLoop
from typing import Union, Any, Optional

import reactivex
import socketio
from reactivex import Observable
from reactivex.abc import ObserverBase, DisposableBase, SchedulerBase
from reactivex.disposable import Disposable
from reactivex.scheduler.eventloop import AsyncIOScheduler

from app.unpackers import unpack_trade, unpack_price

logging.basicConfig(level=logging.DEBUG)


def connect(loop: asyncio.AbstractEventLoop) -> Observable[dict[str, Union[str, float]]]:
    def __sub(observer: Observable[dict[str, Union[str, float]]], scheduler: Optional[SchedulerBase]) -> DisposableBase:
        task = asyncio.run_coroutine_threadsafe(subscription(observer), loop)

        # noinspection PyTypeChecker
        return Disposable(action=task.cancel)




    return reactivex.create(__sub)


async def subscription(observer: ObserverBase[dict[str, Union[str, float]]]):
    sio = socketio.AsyncClient(logger=True)

    def handle_message(message: str):
        message_type = message[0: message.index("~")]
        try:
            if message_type == "0":
                unpacked_message = unpack_trade(message)
                observer.on_next(unpacked_message)
            elif message_type == "5":
                unpacked_message = unpack_price(message)
                observer.on_next(unpacked_message)
        except Exception as e:
            pass

    sio.on("m", handler=handle_message)

    await sio.connect("https://streamer.cryptocompare.com", transports=["websocket"])
    await sio.emit("SubAdd", data={"subs": ["5~CCCAGG~BTC~USD", "0~Coinbase~BTC~USD", "0~Cexio~BTC~USD"]})

    try:
        await sio.wait()
    except asyncio.CancelledError:
        await sio.disconnect()
        observer.on_completed()
    except Exception as e:
        await sio.disconnect()
        observer.on_error(e)




if __name__ == "__main__":
    loop: AbstractEventLoop = asyncio.new_event_loop()

    connect(loop).subscribe(on_next=print, scheduler=AsyncIOScheduler(loop=loop))

    print("Starting")
    loop.run_forever()
