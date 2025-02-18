import time

from weather_station_app.data_analyzer import calculate_stats
from weather_station_app.data_fetcher import read
from weather_station_app.data_parser import parse_data

if __name__ == '__main__':
    (read("weather_stations.csv")
     .pipe(parse_data,
           calculate_stats
           )
     .subscribe(on_next=print))
    time.sleep(100000000)
