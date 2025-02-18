from typing import Union

from reactivex import Observable, operators as ops

from app.mappers import Message, is_trade_message_type, map_to_trade_message

def process(source: Observable[dict[str, Union[str, float]]]) -> Observable[Message[float]]:
    return source.pipe(ops.filter(is_trade_message_type),
                       ops.map(map_to_trade_message))
