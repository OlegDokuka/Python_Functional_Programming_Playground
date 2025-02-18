import dataclasses
import pyrsistent

from pyrsistent import pvector, pmap, PMap, v
from toolz import pipe, juxt


@dataclasses.dataclass
class RawData:
    data: str


@dataclasses.dataclass
class StationData:
    station_name: str
    temperature: float


@dataclasses.dataclass
class StationStats:
    station_name: str
    temperature_min: float
    temperature_max: float
    temperature_avg: float
    temperatures: pvector

    def add_measurement(self, temperature: float) -> "StationStats":
        new_temperatures_list = self.temperatures.append(temperature)
        (vmin, vmax, avg) = pipe(new_temperatures_list,
                                 juxt(min, max, lambda data: sum(data) / len(data))
                                 )
        return StationStats(self.station_name, vmin, vmax, avg, new_temperatures_list)
