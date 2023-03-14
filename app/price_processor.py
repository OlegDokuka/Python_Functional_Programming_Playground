from typing import Union

from reactivex import Observable, operators as ops

from app.mappers import is_price_message_type, Message, is_valid_price_message, map_to_price_message


def process(source: Observable[dict[str, Union[str, float]]]) -> Observable[Message[float]]:
    return source.pipe(ops.filter(lambda x: is_price_message_type(x)),
                       ops.filter(lambda x: is_valid_price_message(x)),
                       ops.map(lambda x: map_to_price_message(x)))
