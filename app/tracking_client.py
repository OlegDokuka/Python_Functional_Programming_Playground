import asyncio
from typing import Union, Any, Coroutine

import reactivex
import socketio  # type: ignore
from reactivex import Observable
from reactivex.abc import ObserverBase
from reactivex.disposable import Disposable

from app.unpackers import unpack_trade, unpack_price


def connect(subscription_loop: asyncio.AbstractEventLoop) -> Observable[dict[str, Union[str, float]]]:
    def on_subscribe(observer: ObserverBase[dict[str, Union[str, float]]], scheduler):
        print("subscribed")
        # we need to call threadsafe run because asyncio loop will not see the scheduled work
        subscription_task = asyncio.run_coroutine_threadsafe(_connect_to_cryptocompare(observer), loop=subscription_loop)

        return Disposable(lambda: subscription_task.cancel())

    # "https://streamer.cryptocompare.com"
    return reactivex.create(on_subscribe)


async def _connect_to_cryptocompare(observer: ObserverBase[dict[str, Union[str, float]]]):
    sio = socketio.AsyncClient()

    @sio.on("m")
    def handle_message(message: str):
        message_type = message[0: message.index("~")]

        if message_type == "0":
            observer.on_next(unpack_trade(message))
        elif message_type == "5":
            observer.on_next(unpack_price(message))

    await sio.connect("https://streamer.cryptocompare.com")
    await sio.emit("SubAdd", data={"subs": ["5~CCCAGG~BTC~USD", "0~Coinbase~BTC~USD", "0~Cexio~BTC~USD"]})

    try:
        await sio.wait()
        observer.on_completed()
    except asyncio.CancelledError:
        print("disconnecting")
        await sio.disconnect()
        print("disconnected")
    except Exception as e:
        print("disconnecting")
        await sio.disconnect()
        observer.on_error(e)
        print("disconnected")


async def await_and_cancel():
    disposable = connect(asyncio.get_running_loop()).subscribe(on_next=print)
    await asyncio.sleep(5)
    print("cancelling task")

    disposable.dispose()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    loop.create_task(await_and_cancel())

    loop.run_forever()
