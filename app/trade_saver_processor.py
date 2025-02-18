import sqlite3
import uuid
from sqlite3 import Connection, Cursor, Row
from typing import Callable

import reactivex
from reactivex import Observable, operators as ops, scheduler

from app.mappers import Message, Trade

scheduler = scheduler.ThreadPoolScheduler(1)
connection_observable: Observable[Connection] = (reactivex.from_callable(lambda: sqlite3.connect('test.db'))
                                                 .pipe(ops.subscribe_on(scheduler)))

def execute(cmd: str) -> Callable[[Observable[Connection]], Observable[Connection]]:
    return lambda cn_obs: cn_obs.pipe(ops.flat_map(_ex(cmd)),
                                      ops.map(lambda cu: cu.connection))


def query(query_string: str) -> Callable[[Observable[Connection]], Observable[Row]]:
    return lambda cn_obs: cn_obs.pipe(ops.flat_map(_ex(query_string)),
                                      ops.flat_map(reactivex.from_iterable))


def commit() -> Callable[[Observable[Connection]], Observable[Connection]]:
    return lambda cn_obs: cn_obs.pipe(ops.map(lambda c: c.commit() or c))


def _ex(query_string: str) -> Callable[[Connection], Observable[Cursor]]:
    return lambda cn: reactivex.defer(lambda s: reactivex.start(lambda: cn.execute(query_string), s))


def store_trade(c: Connection, trade: Message[Trade]):
    id = str(uuid.uuid4())
    c.execute(
        f"INSERT INTO trades (id, trade_timestamp, price, amount, currency, market) VALUES ('{id}', {trade.timestamp}, {trade.data.price}, {trade.data.amount}, '{trade.currency}', '{trade.market}')")
    c.commit()


def save(source: Observable[Message[Trade]]) -> Observable[None]:
    return (connection_observable.pipe(
        execute(
            '''CREATE TABLE IF NOT EXISTS trades 
               (id varchar(48), 
                trade_timestamp long,
                price float,
                amount float,
                currency varchar(8),
                market varchar(64))'''),
        ops.flat_map(
            lambda connect: source.pipe(ops.observe_on(scheduler), ops.map(lambda trade: store_trade(connect, trade)))),
        ops.ignore_elements()
    ))
