import asyncio

from aiostream import pipe
from aiostream.stream import iterate, call

from jobs_app.adzuna_data_classes import AdzunaAppCredentials
from jobs_app.analyzer import recalculate_stats_async
from jobs_app.db_ops import insert_jobs, update_adzuna_credentials, get_all_credentials
from jobs_app.jobs_scrapper import fetch_jobs
from jobs_app.operators import leasing, counting, do_action_with_backpressure


async def _update_adzuna_credentials(resource: tuple[AdzunaAppCredentials, int]):
    await update_adzuna_credentials(resource[0])

async def main():
    xs = (call(get_all_credentials)
          | pipe.delay(0.2)
          | pipe.cycle()
          | pipe.flatten()
          | counting.pipe(lambda source: (
                    source
                    | leasing.pipe(dataminer_fn=lambda resource: fetch_jobs("gb", resource[1], resource[0]),
                                   lease_fn=lambda resource: (resource[0].register_request(), resource[1]),
                                   recycler_fn=_update_adzuna_credentials)
                    | pipe.amap(insert_jobs, task_limit=1)
                    # | pipe.takewhile(lambda jobs: len(jobs) > 0)
                    | pipe.flatmap(lambda jobs: iterate(jobs))
            ))
          | do_action_with_backpressure.pipe(recalculate_stats_async)
          )

    await xs
        # print(el)

    # async with aiohttp.ClientSession(base_url='https://api.adzuna.com') as session:
    #     async for job in fetch_jobs("gb", 0, AdzunaAppCredentials("d3112e8a", "e40d08cb34f37b1b2453a9f3a4575b84")):
    #         print(job["id"])


if __name__ == '__main__':
    asyncio.run(main())