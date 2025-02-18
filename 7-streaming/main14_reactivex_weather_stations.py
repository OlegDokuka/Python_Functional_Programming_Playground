import asyncio
import dataclasses
import time
from typing import Generator

import aiohttp
import reactivex
from pyrsistent import pvector, pmap, PMap, v
from reactivex import operators as ops, Observable
from reactivex.abc import ObserverBase
from reactivex.disposable import Disposable
from reactivex.scheduler import ThreadPoolScheduler
from toolz import pipe, juxt


if __name__ == '__main__':
    shared_scheduler = ThreadPoolScheduler()
    (FileReader.read("../weather_station_app/weather_stations.csv", shared_scheduler)
    .pipe(
        lambda source: DataParser.parse_data(source, shared_scheduler, max_concurrency=10),
        lambda source: DataAnalyzer.calculate_stats(source, shared_scheduler)
    )
    .subscribe(print))

    time.sleep(100)

