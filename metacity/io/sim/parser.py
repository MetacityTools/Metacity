from typing import List
from metacity.datamodel.object import Object
import metacity.geometry as p
from metacity.filesystem.base import read_json

class MultiTimePoint():
    def __init__(self):
        self.geometry = ""
        self.start_time = 0
    
    def parse(self, data):
        self.geometry = data["geometry"]
        self.start_time = data["meta"]["start"]

    def to_models(self):
        model = p.MultiTimePoint()
        model.set_points_from_b64(self.geometry)
        model.set_start_time(self.start_time)
        return [model]


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
    srs.geometry = parse_multi_time_point(data)
    srs.meta = data["meta"]
    return srs


def parse_data(data):
    sl = SeriesList()
    for el in data:
        series_object = parse_series(el)
        sl.series.append(series_object)
    objects = sl.to_objectlist()
    return objects


def parse(input_file: str):
    contents = read_json(input_file)
    return parse_data(contents)