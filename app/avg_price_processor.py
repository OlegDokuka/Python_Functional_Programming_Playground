from functools import reduce
from typing import List, Callable, Tuple, Any, Union

from reactivex import Observable, operators as ops

from app.mappers import Message


def process(source: Observable[Message[float]], average_interval_setting: Observable[float]) -> Observable[
    Message[float]]:
    # stream: AsyncIterable[Message[float]]
    # queue: list[Message[float]] = []
    # async for message in stream:
    #     if len(queue) > 0 and message.timestamp - queue[0].timestamp > 30_000:
    #         total = 0
    #         for stored in queue:
    #             total += stored.data
    #
    #         yield total / len(queue)
    #     else:
    #         queue.append(message)

    reducer_fn: Callable[[tuple[int, float], Message[float]], tuple[int, float]] = lambda state, next_msg: (
        state[0] + 1, state[1] + next_msg.data)
    # reduce_to_count_and_total: Callable[[List[Message[float]]], Tuple[int, float]] = lambda collected_events: reduce(
    #     reducer_fn, collected_events, (0, 0))

    observable_reduce_to_count_and_total: Callable[[Observable[Message[float]]], Observable[Tuple[int, float]]] = \
        lambda collected_events: collected_events.pipe(ops.reduce(reducer_fn, (0, 0)))

    calculate_avg: Callable[[tuple[int, float]], Any] = lambda result: result[1] / result[0]

    return average_interval_setting.pipe(
        ops.map(lambda interval_setting:
                source.pipe(ops.window_with_time(interval_setting),
                            ops.flat_map(lambda window: window.pipe(
                                ops.group_by(lambda msg: msg.currency),
                                ops.flat_map(lambda
                                                 groped_messages_obs: groped_messages_obs.pipe(
                                    observable_reduce_to_count_and_total,
                                    ops.map(calculate_avg),
                                    ops.map(lambda avg: Message.avg(avg,
                                                                    groped_messages_obs.key,
                                                                    "Local"))))
                            )))),
        ops.switch_latest())
