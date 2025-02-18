import time
from typing import Generator

import reactivex
from reactivex import operators as ops, Observable
from reactivex.scheduler import ThreadPoolScheduler


def read(filename: str, scheduler = ThreadPoolScheduler()) -> Observable[str]:
    return (reactivex.defer(lambda sb: reactivex.from_iterable(read_lines(filename)))
            .pipe(ops.subscribe_on(scheduler),
                  ops.observe_on(scheduler)))


def read_lines(filename: str) -> Generator[str, None, None]:
    with open(filename, 'r', encoding='UTF-8') as file:
        while line := file.readline():
            yield line.rstrip()


if __name__ == '__main__':
    # print([line for line in read_lines('weather_stations.csv')])

    (read('weather_stations.csv')
     .pipe(ops.do_action(on_next=print))
     .subscribe())


    time.sleep(100000000)
