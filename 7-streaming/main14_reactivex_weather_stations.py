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


@dataclasses.dataclass
class RawData:
    data: str


@dataclasses.dataclass
class StationData:
    station_name: str
    temperature: float


@dataclasses.dataclass
class StationStats:
    station_name: str
    temperature_min: float
    temperature_max: float
    temperature_avg: float
    temperatures: pvector

    def add_measurement(self, temperature: float) -> "StationStats":
        new_temperatures_list = self.temperatures.append(temperature)
        (vmin, vmax, avg) = pipe(new_temperatures_list,
                                 juxt(min, max, lambda data: sum(data) / len(data))
                                 )
        return StationStats(self.station_name, vmin, vmax, avg, new_temperatures_list)


class FileReader:

    @classmethod
    def read(cls, filename: str, scheduler) -> Observable[str]:
        return (reactivex.defer(lambda schd: reactivex.from_iterable(cls._read(filename), schd))
                .pipe(ops.subscribe_on(scheduler)))

    @classmethod
    def _read(cls, filename: str) -> Generator[str, None, None]:
        with open(filename, 'r', encoding='UTF-8') as file:
            while line := file.readline():
                yield line.rstrip()
                print("produced message")


class DataParser:
    @staticmethod
    def _parse(raw_data: str) -> Observable[StationData]:
        print(f"received message {raw_data}")
        parts = raw_data.split(";")
        if len(parts) == 2:
            try:
                return reactivex.of(StationData(parts[0], float(parts[1])))
            except Exception as e:
                pass

        return reactivex.empty()

    @classmethod
    def parse_data(cls, messages_stream: Observable[str], scheduler, max_concurrency=10) -> Observable[StationData]:
        return messages_stream.pipe(
            ops.map(lambda raw_data: reactivex.defer(lambda s: cls._parse(raw_data)).pipe(ops.subscribe_on(scheduler))),
            ops.merge(max_concurrent=max_concurrency)
        )


class DataAnalyzer:
    @staticmethod
    def analyze(state: PMap[str, StationStats], msg: StationData) -> PMap[str, StationStats]:
        # print(f"received message {msg}")
        if not msg.station_name in state:
            return state.set(msg.station_name, StationStats(
                msg.station_name,
                msg.temperature,
                msg.temperature,
                msg.temperature,
                v(msg.temperature)
            ))
        else:
            return state.set(msg.station_name, state[msg.station_name].add_measurement(msg.temperature))

    @classmethod
    def calculate_stats(cls, messages_stream: Observable[StationData], scheduler):
        return messages_stream.pipe(
            ops.observe_on(scheduler),
            ops.scan(cls.analyze, pmap())
        )


if __name__ == '__main__':
    shared_scheduler = ThreadPoolScheduler()
    (FileReader.read("./weather_stations.csv", shared_scheduler)
    .pipe(
        lambda source: DataParser.parse_data(source, shared_scheduler, max_concurrency=10),
        lambda source: DataAnalyzer.calculate_stats(source, shared_scheduler)
    )
    .subscribe(print))

    time.sleep(100)

