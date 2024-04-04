import asyncio
from typing import Generator

import aiohttp
from aiohttp import ClientSession


async def fetch_data(session: ClientSession):
    async with session.get('https://api.github.com/events') as resp:
        return await resp.json()


async def populate_db(json):
    return await asyncio.sleep(1)
async def populate_db2(json):
    return await asyncio.sleep(1)


async def stream_data() -> Generator[dict]:
    async with aiohttp.ClientSession() as session:
        while True:
            yield await fetch_data(session)
            await asyncio.sleep(1)


async def main():
    # Schedule three calls *concurrently*:
    async for result in stream_data():
        print(result)  ## assume this is an analysis step
        await asyncio.gather(populate_db(result), populate_db2(result))
        print(result)


if __name__ == '__main__':
    asyncio.run(main())
