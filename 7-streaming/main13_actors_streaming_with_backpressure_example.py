import dataclasses
import logging
import time

# import pipe as pp
from thespian.troupe import troupe
from toolz import curry, pipe, juxt
from toolz.curried import get
from pyrsistent import v, pvector, plist

from thespian.actors import *

from logsetup import logcfg


@dataclasses.dataclass
class OpenFileRequest:
    filename: str
    recipient: ActorAddress
    parser: ActorAddress
    analyzer: ActorAddress


@dataclasses.dataclass
class ReadMoreRequest:
    quantity: int


@dataclasses.dataclass
class CloseFileRequest:
    ...


@dataclasses.dataclass
class RawData:
    data: str
    recipient: ActorAddress
    analyzer: ActorAddress
    filereader: ActorAddress


@dataclasses.dataclass
class StationData:
    station_name: str
    temperature: float


@dataclasses.dataclass
class StationDataMsg:
    data: StationData
    recepient: ActorAddress
    filereader: ActorAddress


@dataclasses.dataclass
class StationStats:
    station_name: str
    temperature_min: float
    temperature_max: float
    temperature_avg: float
    temperatures: pvector

    def add_measurement(self, temperature: float ) -> "StationStats":
        new_temperatures_list = self.temperatures.append(temperature)
        (vmin, vmax, avg) = pipe(new_temperatures_list,
                                 juxt(min, max, lambda data: sum(data) / len(data))
                                 )
        return StationStats(self.station_name, vmin, vmax, avg, new_temperatures_list)


class Acceptor(ActorTypeDispatcher):
    def __init__(self, *args, **kw):
        super(Acceptor, self).__init__(*args, **kw)
        # The analyzer and encoders will be Actor Addresses; these
        # cannot be created now because the Acceptor has not been
        # fully initialized into the ActorSystem until after the
        # __init__ has finished.
        self.filereader = None
        self.dataparser = None
        self.dataanalyzer = None

    def receiveMsg_str(self, file, sender):
        if not self.filereader:
            self.filereader = self.createActor(FileReader)
        if not self.dataparser:
            self.dataparser = self.createActor(DataParser)
        if not self.dataanalyzer:
            self.dataanalyzer = self.createActor(DataAnalyzer)

        self.send(self.filereader, OpenFileRequest(file, sender, self.dataparser, self.dataanalyzer))


class FileReader(ActorTypeDispatcher):

    def __init__(self):
        super().__init__()
        self.recipient = None
        self.analyzer = None
        self.opened_file = None
        self.parser = None

    def receiveMsg_OpenFileRequest(self, message: OpenFileRequest, sender):
        self.opened_file = open(message.filename, 'r', encoding='UTF-8')
        self.parser = message.parser
        self.analyzer = message.analyzer
        self.recipient = message.recipient

        for i in range(0, 100):
            if line := self.opened_file.readline():
                self.send(self.parser, RawData(line.rstrip(), self.recipient, self.analyzer, self.myAddress))
                print("produced message")

    def receiveMsg_ReadMoreRequest(self, message: ReadMoreRequest, sender):
        for i in range(0, message.quantity):
            if line := self.opened_file.readline():
                self.send(self.parser, RawData(line.rstrip(), self.recipient, self.analyzer, self.myAddress))
                print("produced message")

    def receiveMsg_CloseFileRequest(self, message: CloseFileRequest, sender):
        self.opened_file.close()


@troupe(10)
class DataParser(ActorTypeDispatcher):
    def receiveMsg_RawData(self, message: RawData, sender):
        time.sleep(0.1)
        print(f"received message {message}")
        rawdata = message.data
        parts = rawdata.split(";")
        if len(parts) == 2:
            try:
                self.send(message.analyzer, StationDataMsg(StationData(parts[0], float(parts[1])), message.recipient, message.filereader))
            except Exception as e:
                pass


class DataAnalyzer(ActorTypeDispatcher):
    data: dict[str, StationStats] = {}
    counter: int = 0
    limit: int = 75

    def receiveMsg_StationDataMsg(self, msg: StationDataMsg, sender):
        # print(f"received message {msg}")
        if not msg.data.station_name in self.data:
            self.data[msg.data.station_name] = StationStats(
                msg.data.station_name,
                msg.data.temperature,
                msg.data.temperature,
                msg.data.temperature,
                v(msg.data.temperature)
            )
        else:
            self.data[msg.data.station_name] = self.data[msg.data.station_name].add_measurement(msg.data.temperature)

        # print(f"send message {self.data[msg.data.station_name]}")
        self.send(msg.recepient, self.data[msg.data.station_name])

        self.counter = self.counter + 1

        if self.counter == self.limit:
            self.counter = 0
            self.send(msg.filereader, ReadMoreRequest(self.limit))

        # 1. update data and add new measurement
        # 2. recalculate min/avg/max
        # 3. send new update to final recipient


def main(systembase=None):
    # asys = ActorSystem(systembase, logDefs=logcfg)
    asys = ActorSystem(systembase)
    # Schedule three calls *concurrently*:
    acceptor = ActorSystem().createActor(Acceptor)
    ActorSystem().tell(acceptor, "./weather_stations.csv")

    for i in range(1000):
        print(ActorSystem().listen())


if __name__ == '__main__':
    main()
