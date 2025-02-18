from pyrsistent import PMap, v, pmap
from reactivex import operators as ops, Observable

from weather_station_app.data_model import StationStats, StationData


def analyze(state: PMap[str, StationStats], msg: StationData) -> PMap[str, StationStats]:
    if not msg.station_name in state:
        return state.set(msg.station_name, StationStats(
            msg.station_name,
            msg.temperature,
            msg.temperature,
            msg.temperature,
            v(msg.temperature)
        ))
    else:
        return state.set(msg.station_name, state[msg.station_name].add_measurement(msg.temperature))

def calculate_stats(messages_stream: Observable[StationData]):
    return messages_stream.pipe(ops.reduce(analyze, pmap()))