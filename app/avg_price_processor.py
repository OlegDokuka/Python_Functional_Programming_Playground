import time
from typing import Callable, Tuple, Any, AsyncIterable, List

from future.backports.datetime import timedelta
from reactivex import Observable, operators as ops

from app.mappers import Message


def process(source: Observable[Message[float]], average_interval_setting: Observable[float]) -> Observable[Message[float]]:

    # async def processor(live_source: AsyncIterable[Message[float]], periodStream: AsyncIterable[int]) ->  AsyncIterable[Message[float]]:
        # window_start_ns = time.time_ns()
        # counter = dict()
        # total = dict()
        # async for period in periodStream:
        #     async for message in live_source:
        #         counter.get(message.currency)
        #
        #         counter += 1
        #         total += message.data
        #         current_time = time.time_ns()
        #
        #         if current_time - window_start_ns >= period:
        #             counter.clear()
        #             total.clear()
        #             yield Message.avg(total / counter, "???", "Local")

    return (average_interval_setting
            .pipe(ops.flat_map_latest(lambda new_period:
                  (source
                   .pipe(ops.window_with_time(timedelta(seconds=new_period)),
                         ops.flat_map(lambda stream:
                                      stream.pipe(ops.group_by(
                                          lambda message: message.currency),
                                                  ops.flat_map(lambda
                                                                   gstream: calculate_avg_price(
                                                      gstream, gstream.key))))
                         ))
                  )))



def calculate_avg_price(elements_observer_during_period: Observable[Message[float]], currency: str) -> Observable[Message[float]]:
    def calc(state: Tuple[int, float], message: Message[float]) -> Tuple[int, float]:
        return tuple(state[0] + 1, state[1] + message.data)

    return (elements_observer_during_period
            .pipe(ops.reduce(calc, tuple(0, 0.0)),
                  ops.map(lambda avg: Message.avg(avg[1] / avg[0], currency, "Local"))))


