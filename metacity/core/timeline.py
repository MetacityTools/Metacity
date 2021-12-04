from typing import Dict, List
from metacity.datamodel.layer import Layer
from metacity.datamodel.set import desermodel
from metacity.datamodel.set import DataSet
import metacity.filesystem.timeline as fs
from metacity.geometry import BaseModel, MultiTimePoint
from metacity.geometry import Interval
from metacity.utils.persistable import Persistable
from tqdm import tqdm



class IntervalSet(DataSet):
    def __init__(self, timeline_dir: str, start_time: int, offset: int, capacity: int):        
        super().__init__(fs.timeline_cache_interval_dir(timeline_dir, start_time), offset, capacity)

    def serialize(self): 
        data = super().serialize()
        models = []
        model: MultiTimePoint
        for model in self.data:
            models.append(model.serialize())
        data['models'] = models
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.data = []
        for model in data['models']:
            self.data.append(desermodel(model))



class IntervalCache:
    def __init__(self, timeline_dir: str, start_time: int, end_time: int, group_by=100):
        self.start_time = start_time
        self.end_time = end_time
        self.timeline_dir = timeline_dir
        self.size = 0
        self.group_by = group_by
        self.set = IntervalSet(self.timeline_dir, self.start_time, 0, self.group_by)

    def add(self, oid: int, model: MultiTimePoint):
        if not self.set.can_contain(self.size):
            self.set.export()
            self.activate_set(self.size)
        model.add_tag("oid", oid)
        self.set.add(model)
        self.size += 1

    def __getitem__(self, index: int):
        if not self.set.can_contain(index):
            self.set.export()
            self.activate_set(index)
        obj: MultiTimePoint = self.set[index]
        return obj

    def activate_set(self, index):
        offset = (index // self.group_by) * self.group_by
        self.set = IntervalSet(self.timeline_dir, self.start_time, offset, self.group_by)

    @property
    def models(self):
        for i in range(self.size):
            yield self[i]

    def to_interval(self):
        movement_count = 0
        output = fs.interval(self.timeline_dir, self.start_time)
        output_stream = fs.interval_stream(self.timeline_dir, self.start_time)
        interval = Interval(self.start_time, self.end_time - self.start_time)
        
        for model in self.models:
            movement_count += interval.insert(model, model.tags["oid"])
                
        fs.base.write_json(output, interval.serialize())
        fs.base.write_json(output_stream, interval.serialize_stream())
        return movement_count



class Timeline(Persistable):
    def __init__(self, layer: Layer, group_by: int = 60):
        self.dir = fs.timeline_dir(layer.dir)
        self.group_by = group_by
        self.init = False
        self.movement_count = 0
        self.interval = None

        self.cache: Dict[int, IntervalCache] = {}

        super().__init__(fs.timeline_config(self.dir))

        try:
            self.load()
        except FileNotFoundError:
            pass

    def clear(self):
        fs.clear_timeline(self.dir)

    @property
    def intervals(self):
        for interval_file in self.interval_list():
            interval_path = fs.interval_file(self.dir, interval_file)
            yield self.load_existing_interval(interval_path)

    def interval_list(self):
        return fs.interval_list(self.dir)

    def load_existing_interval(self, interval_file: str):
        data = fs.base.read_json(interval_file)
        i = Interval()
        i.deserialize(data)
        return i

    def time_to_interval_start(self, start_time):
        interval_start_time = (start_time // self.group_by) * self.group_by
        return interval_start_time


    def add(self, oid: int, model: MultiTimePoint):
        if model.type != "timepoint":
            return

        submodels = model.slice_to_timeline(self.group_by)

        for model in submodels:
            interval_start = self.time_to_interval_start(model.start_time)
            if interval_start not in self.cache:
                self.cache[interval_start] = IntervalCache(self.dir, interval_start, interval_start + self.group_by)

            self.cache[interval_start].add(oid, model)

    def persist(self, progressCallback=None):
        for cache in self.cache.values():
            self.movement_count += cache.to_interval()
            if progressCallback is not None:
                progressCallback(f"cache {cache.start_time}")

        self.init = True
        self.export()


    def serialize(self):
        return {
            "group_by": self.group_by,
            "init": self.init,
            "movement_count": self.movement_count
        }

    def deserialize(self, data):
        self.group_by = data["group_by"]
        self.init = data["init"]
        self.movement_count = data["movement_count"]


def build_timeline(layer: Layer, interval_length: int = 60, progressCallback=None):
    timeline = Timeline(layer, interval_length)
    timeline.clear()


    for oid, object in enumerate(layer.objects):
        for model in object.models:
            timeline.add(oid, model)

    timeline.persist(progressCallback)
    return timeline

