from asyncio import Task, Future

import asyncio
from typing import AsyncIterable, Callable, Awaitable, Tuple, TypeVar, AsyncIterator, Any
from typing import AsyncIterable, Callable, Awaitable, Tuple, TypeVar, AsyncIterator

from aiostream import streamcontext, pipable_operator, operator, await_, pipe

R = TypeVar("R")
T = TypeVar("T")
K = TypeVar("K")


@pipable_operator
async def leasing(resources: AsyncIterable[R], dataminer_fn: Callable[[R], AsyncIterable[T]],
                  lease_fn: Callable[[R], R], recycler_fn: Callable[[R], Awaitable[None]]) -> AsyncIterator[T]:
    async with streamcontext(resources) as streamer:
        async for resource in streamer:
            local_resource = resource
            stream = dataminer_fn(resource).__aiter__()
            while True:
                # noinspection PyBroadException
                try:
                    local_resource = lease_fn(local_resource)
                    yield await stream.__anext__()
                except Exception as e:
                    await recycler_fn(local_resource)
                    break


@pipable_operator
async def counting(source: AsyncIterable[T],
                   mapper: Callable[[AsyncIterable[Tuple[T, int]]], AsyncIterable[K]]) -> AsyncIterator[K]:
    async with streamcontext(source) as streamer:
        count: int = 0

        @operator
        async def _generate() -> AsyncIterable[Tuple[T, int]]:
            async for t_item in streamer:
                yield t_item, count

        async for k_item in mapper(_generate()):
            count += 1
            yield k_item


# Main coroutine consuming async iterable and controlling the background task
@pipable_operator
async def do_action_with_backpressure(source: AsyncIterable[T],
                                      action: Callable[[], Awaitable[None]]) -> AsyncIterator[T]:
    async with streamcontext(source) as streamer:
        task: Task[None] | None = None
        need_restart = 0

        def handle_task_completion(_: Any):
            nonlocal task, need_restart
            if need_restart > 0:
                need_restart = 0
                task = asyncio.create_task(action())
                task.add_done_callback(handle_task_completion)


        async for item in streamer:

            if task is None or task.done():
                need_restart = 0
                task = asyncio.create_task(action())
                task.add_done_callback(handle_task_completion)
            else:
                need_restart += 1

            yield item


if __name__ == '__main__':

    # Async generator producing an infinite number of elements
    @operator
    async def async_generator():
        i = 1
        while True:
            for j in range(1, 20):
                await asyncio.sleep(0.1)  # Simulate delay
                yield i
                i += 1

            # await asyncio.sleep(10)


    # Background async task that runs intermittently
    async def background_task():
        print("Background task started...")
        await asyncio.sleep(3)  # Simulating some work
        print("Background task completed.")


    async def main():
        await (async_generator()
               | do_action_with_backpressure.pipe(background_task)
               | pipe.print()
               )


    asyncio.run(main())
