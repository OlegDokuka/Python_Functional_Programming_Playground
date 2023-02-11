import asyncio
import aiohttp
from aiohttp import ClientSession


async def fetch_data(session: ClientSession):
    async with session.get('https://api.github.com/events') as resp:
        return await resp.json()


async def stream_data():
    async with aiohttp.ClientSession() as session:
        while True:
            yield await fetch_data(session)
            await asyncio.sleep(1)


async def main():
    # Schedule three calls *concurrently*:
    async for result in stream_data():
        print(result)


if __name__ == '__main__':
    asyncio.run(main())
