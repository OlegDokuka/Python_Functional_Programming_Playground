import asyncio
import json
import re
from collections import deque
from datetime import datetime
from functools import partial
from typing import List, AsyncIterable

import aiosqlite

from jobs_app.adzuna_data_classes import Job, AdzunaAppCredentials


async def create_jobs_table():
    async with aiosqlite.connect("adzuna.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                description TEXT,
                contract_time TEXT,
                longitude REAL,
                location TEXT,
                country TEXT,
                salary_min INTEGER,
                created TEXT,
                contract_type TEXT,
                salary_is_predicted TEXT,
                adref TEXT,
                latitude REAL,
                redirect_url TEXT,
                title TEXT,
                salary_max INTEGER,
                company TEXT,
                category TEXT
            )
        ''')
        await db.commit()


async def create_api_credentials_table():
    async with aiosqlite.connect("adzuna.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS adzuna_app_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_id TEXT NOT NULL UNIQUE,
                app_key TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                requests TEXT
            )
        ''')
        await db.commit()


async def update_adzuna_credentials(credentials: AdzunaAppCredentials) -> None:
    """
    Updates a record in the adzuna_app_credentials table based on the given AdzunaAppCredentials object.

    Args:
        credentials (AdzunaAppCredentials): The object containing the updated data to apply.
    """
    async with aiosqlite.connect("adzuna.db") as db:  # Replace 'database.db' with the actual database name
        await db.execute(
            """
            UPDATE adzuna_app_credentials
            SET
                requests = ?
            WHERE app_id = ?
            """,
            (','.join(map(lambda dt: str(dt.timestamp()), credentials.requests)), credentials.app_id)
        )
        await db.commit()  # Commit changes to the database


async def get_all_credentials() -> AsyncIterable[AdzunaAppCredentials]:
    """
    Reads all the rows from the adzuna_app_credentials table and maps them to AdzunaAppCredentials instances.

    Returns:
        List[AdzunaAppCredentials]: A list of AdzunaAppCredentials instances.
    """
    credentials = []
    pattern = r"^-?\d+\.\d+$"
    async with aiosqlite.connect("adzuna.db") as db:  # Replace 'database.db' with the actual database name
        async with db.execute("SELECT app_id, app_key, requests FROM adzuna_app_credentials") as cursor:
            async for row in cursor:
                # Map each row to an AdzunaAppCredentials object
                credential = AdzunaAppCredentials(
                    app_id=row[0],
                    app_key=row[1],
                    requests=deque(map(lambda ts: datetime.fromtimestamp(float(ts)), filter(lambda s: re.match(pattern, s), row[2].split(","))))
                )
                credentials.append(credential)

    for credential in credentials:
        yield credential


async def insert_jobs(jobs: List[Job]) -> List[Job]:
    successfully_inserted_jobs = []
    async with aiosqlite.connect("adzuna.db") as db:
        for job in jobs:
            try:
                cursor = await db.execute('''
                    INSERT OR IGNORE INTO jobs (
                        id, description, contract_time, longitude, location, salary_min,
                        created, contract_type, salary_is_predicted, adref, latitude,
                        redirect_url, title, salary_max, company, category, country
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    job.id, job.description, job.contract_time, job.longitude, job.location.display_name,
                    job.salary_min, job.created, job.contract_type, job.salary_is_predicted,
                    job.adref, job.latitude, job.redirect_url, job.title,
                    job.salary_max, job.company.display_name, job.category.tag, job.country
                ))

                # If a row was inserted, cursor.rowcount will be 1
                if cursor.rowcount > 0:
                    successfully_inserted_jobs.append(job)
            except Exception as e:
                print(e)

            await db.commit()

    return successfully_inserted_jobs


if __name__ == '__main__':
    asyncio.run(create_api_credentials_table())
    asyncio.run(create_jobs_table())
