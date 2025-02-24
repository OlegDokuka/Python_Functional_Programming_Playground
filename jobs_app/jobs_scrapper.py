import asyncio
import resource
from typing import AsyncGenerator, Iterable, List, AsyncIterator, AsyncIterable

import aiohttp
from aiohttp import ClientSession, ClientResponse
from aiostream.stream import iterate, create
from aiostream import pipe, await_, pipable_operator, Stream

from jobs_app.adzuna_data_classes import AdzunaAppCredentials, JobSearchResults, Job
from jobs_app.db_ops import insert_jobs, update_adzuna_credentials
from jobs_app.operators import leasing, counting

jobs_per_page = 10

async def fetch_jobs_page(session: ClientSession, country: str, page: int,
                          credentials: AdzunaAppCredentials) -> JobSearchResults:
    resp: ClientResponse
    async with session.get(
            f'/v1/api/jobs/{country}/search/{page}?app_id={credentials.app_id}&app_key={credentials.app_key}&sort_by=date') as resp:
        if resp.status != 200:
            raise RuntimeError(f"Error fetching page:\n{await resp.text()}")
        json_result = await resp.json()
        return JobSearchResults.from_dict(json_result, country)


async def fetch_jobs(country: str, fetched_jobs_cnt: int, credentials: AdzunaAppCredentials) -> AsyncGenerator[Iterable[Job], None]:
    try:
        async with aiohttp.ClientSession(base_url='https://api.adzuna.com') as session:
            page_number = int(fetched_jobs_cnt / jobs_per_page) + 1
            while True:
                fetched_jobs = await fetch_jobs_page(session, country, page_number, credentials)
                page_number = page_number + 1

                yield fetched_jobs.results

                if fetched_jobs.count <= page_number * jobs_per_page:
                    break
    except Exception as e:
        print(e)