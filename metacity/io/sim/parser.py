import json
from typing import List, Union
from metacity.datamodel.object import Object
import metacity.geometry as p

class MultiTimePoint():
    def __init__(self):
        self.coordinates = []

    def parse(self, data):
        ...

    def to_models(self):
        ...



class Series:
    def __init__(self):
        self.meta = {}
        self.geometry: MultiTimePoint = None

    def to_object(self):
        o = Object()
        o.models = self.geometry.to_models()
        o.meta = self.meta
        return o

class SeriesList:
    def __init__(self):
        self.series: List[Series] = []

    def to_objectlist(self):
        objects = [s.to_object() for s in self.series]
        return objects

def parse_multi_time_point(data):
    model = MultiTimePoint()
    model.parse(data)
    return model


def parse_series(data):
    srs = Series()
    if "meta" in data:
        srs.meta = data["meta"]
    if "geometry" in data:
        srs.geometry = parse_multi_time_point(data["geometry"])
    return srs

def parse_data(data):
    sl = SeriesList()
    for el in data:
        series_object = parse_series(el)
        sl.series.append(series_object)
    objects = sl.to_objectlist()
    return objects


def parse(input_file: str):
    with open(input_file, 'r') as file:
        contents = json.load(file)
    return parse_data(contents)

def main():
    input_file = "/home/metakocour/Projects/Metacity/metacity/io/sim/subway_sec_0.json"
    with open(input_file, 'r') as file:
        contents = json.load(file)
    
if __name__ == "__main__":
    main()
