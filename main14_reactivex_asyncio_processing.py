import asyncio

import aiohttp
import reactivex
from reactivex import operators as ops, Observable
from reactivex.abc import ObserverBase
from reactivex.disposable import Disposable


async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com/events') as resp:
            return await resp.json()


def main(loop):
    def on_subscribe(observer: ObserverBase[str], scheduler):
        task = asyncio.run_coroutine_threadsafe(fetch_data(), loop=loop)

        def handle_result(result):
            observer.on_next(result.result())
            observer.on_completed()

        task.add_done_callback(handle_result)

        return Disposable(lambda: task.cancel())  # type: ignore

    # (reactivex.create(on_subscribe).subscribe(on_next=print, on_completed=lambda: print("done")))

    source: Observable[int] = reactivex.interval(1)  # type: ignore
    def flatten(i):
        print(i)
        # return reactivex.create(on_subscribe)
        return reactivex.from_future(asyncio.run_coroutine_threadsafe(fetch_data(), loop=loop))
    (source.pipe(ops.flat_map(flatten)).subscribe(on_next=print))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    main(loop)
    loop.run_forever()
