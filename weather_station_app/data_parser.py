import reactivex
from pyrsistent import PMap, v, pmap
from reactivex import operators as ops, Observable

from weather_station_app.data_model import StationStats, StationData

def parse(raw_data: str) -> list[str]:
    return raw_data.split(";")

def check(raw_data_parts: list[str]) -> bool:
    if len(raw_data_parts) == 2:
        try:
            float(raw_data_parts[1])
            return True
        except ValueError:
            return False
    return False

def convert(data_parts: list[str]) -> StationData:
    return StationData(data_parts[0], float(data_parts[1]))


def parse_data(messages_stream: Observable[str]) -> Observable[StationData]:
    return messages_stream.pipe(ops.map(parse),
                                ops.filter(check),
                                ops.map(convert)
                                )


if __name__ == '__main__':
    assert parse("Ta;1.2") == list(["Ta", "1.2"])
    assert check(parse("Ta;1.2"))

    (parse_data(messages_stream=reactivex.from_iterable(["Ta;1.2", "Ba;-12", "Ma;1.2a", "Ta1.2"]))
     .pipe(ops.do_action(on_next=print))
     .subscribe())