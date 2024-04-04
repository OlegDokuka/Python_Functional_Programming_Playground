from typing import Union

from reactivex import Observable, operators as ops

from app.mappers import is_price_message_type, Message, is_valid_price_message, map_to_price_message


def process(source: Observable[dict[str, Union[str, float]]]) -> Observable[Message[float]]:
    return source.pipe(
        ops.filter(is_price_message_type),
        ops.filter(is_valid_price_message),
        ops.map(map_to_price_message)
    )
