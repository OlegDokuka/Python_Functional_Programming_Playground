import sqlite3
import time
from sqlite3 import Connection, Cursor, Row
from typing import Union, Callable

import expression
import reactivex
from reactivex import Observable, operators as ops, scheduler

from app.mappers import Message, is_trade_message_type, map_to_trade_message

connection_observable: Observable[Connection] = (reactivex.from_callable(lambda: sqlite3.connect('test.db'))
                                                 .pipe(ops.subscribe_on(scheduler.NewThreadScheduler())))


def execute(cmd: str) -> Callable[[Observable[Connection]], Observable[Connection]]:
    return lambda cn_obs: cn_obs.pipe(ops.flat_map(_ex(cmd)),
                                      ops.map(lambda cu: cu.connection))


def query(query_string: str) -> Callable[[Observable[Connection]], Observable[Row]]:
    return lambda cn_obs: cn_obs.pipe(ops.flat_map(_ex(query_string)),
                                      ops.flat_map(reactivex.from_iterable))


def commit() -> Callable[[Observable[Connection]], Observable[Connection]]:
    return lambda cn_obs: cn_obs.pipe(ops.map(lambda c: c.commit() or c))


@expression.curry(1)
def _ex(query_string: str, cn: Connection) -> Observable[Cursor]:
    return reactivex.defer(lambda s: reactivex.start(lambda: cn.execute(query_string), s))


if __name__ == "__main__":
    print("Opened database successfully")

    (connection_observable
     .pipe(
        execute(
            '''CREATE TABLE trades 
               (id varchar(48), 
                trade_timestamp long,
                price float,
                amount float,
                currency varchar(8),
                market varchar(64))'''),
        execute(
            "INSERT INTO trades (id, trade_timestamp, price, amount, currency, market) VALUES ($1, $2, $3, $4, $5, $6)"),
        commit(),
        query("SELECT * FROM Employees"))
     .subscribe(on_next=print, on_completed=lambda: print("done"), on_error=lambda e: print(e)))

    time.sleep(10000)


def process(source: Observable[dict[str, Union[str, float]]]) -> Observable[Message[float]]:
    return source.pipe(ops.filter(is_trade_message_type),
                       ops.map(map_to_trade_message))
