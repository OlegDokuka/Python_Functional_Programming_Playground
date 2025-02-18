import asyncio
import concurrent
import time
from concurrent.futures import Future, ProcessPoolExecutor
from typing import Iterator, AsyncIterator


async def factorial(name, number) -> AsyncIterator[int]:
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        yield f
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f

# def when_all_are_done(*futures: Future[int]):
#     for future in futures:
#         print(future.result())

def when_all_are_done(results: Iterator[int]):
    for future in results:
        print(future)

async def main():
    with concurrent.futures.ProcessPoolExecutor(2) as executor:
        future1 = executor.submit(factorial, "A", 3)
        future2 = executor.submit(factorial, "B", 4)

        await asyncio.wrap_future(future1)

    results = await asyncio.gather(
        factorial("A", 3),
        factorial("B", 4)
    )
    when_all_are_done(results)




if __name__ == '__main__':
    asyncio.run(main())
    # main()
