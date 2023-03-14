#!/usr/bin/env python
import dataclasses
import time
from enum import Enum
from typing import TypeVar, Generic, Union

_T = TypeVar("_T")


@dataclasses.dataclass
class Trade:
    price: float
    amount: float


@dataclasses.dataclass
class Message(Generic[_T]):
    timestamp: int
    data: _T
    currency: str
    market: str
    type: 'MessageType'

    @staticmethod
    def avg(avg: float, currency: str, market: str):
        return Message(timestamp=round(time.time() * 1000), data=avg, currency=currency, market=market,
                       type=MessageType.AVG)

    @staticmethod
    def price(price: float, currency: str, market: str):
        return Message(timestamp=round(time.time() * 1000), data=price, currency=currency, market=market,
                       type=MessageType.PRICE)

    @staticmethod
    def trade(timestamp: int, price: float, amount: float, currency: str, market: str):
        return Message(timestamp=timestamp, data=Trade(price=price, amount=amount), currency=currency, market=market,
                       type=MessageType.TRADE)


class MessageType(Enum):
    PRICE = 0
    AVG = 1
    TRADE = 2


""" generated source for class MessageMapper """
TYPE_KEY = "TYPE"
TIMESTAMP_KEY = "TIMESTAMP"
PRICE_KEY = "PRICE"
QUANTITY_KEY = "QUANTITY"
CURRENCY_KEY = "FROMSYMBOL"
MARKET_KEY = "MARKET"
FLAGS_KEY = "FLAGS"


def map_to_price_message(event):
    """ generated source for method mapToPriceMessage """
    return Message.price((event.get(PRICE_KEY)), str(event.get(CURRENCY_KEY)),
                         str(event.get(MARKET_KEY)))


def map_to_trade_message(event):
    """ generated source for method mapToTradeMessage """
    return Message.trade((event.get(TIMESTAMP_KEY)) * 1000, (event.get(PRICE_KEY)),
                         (event.get(QUANTITY_KEY)) if event.get(FLAGS_KEY) == "1" else -(event.get(QUANTITY_KEY)),
                         str(event.get(CURRENCY_KEY)),
                         str(event.get(MARKET_KEY)))


def is_price_message_type(event: dict[str, Union[str, float]]):
    """ generated source for method isPriceMessageType """
    return TYPE_KEY in event and event[TYPE_KEY] == "5"


def is_valid_price_message(event:dict[str, Union[str, float]]):
    """ generated source for method isValidPriceMessage """
    return PRICE_KEY in event and CURRENCY_KEY in event and MARKET_KEY in event


def is_trade_message_type(event:dict[str, Union[str, float]]):
    """ generated source for method isTradeMessageType """
    return TYPE_KEY in event and event[TYPE_KEY] == "0"
