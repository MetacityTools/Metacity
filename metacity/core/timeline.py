from metacity.datamodel.layer import Layer
import metacity.filesystem.timeline as fs
from metacity.geometry import BaseModel
from metacity.geometry import Interval
from metacity.utils.persistable import Persistable


class Timeline(Persistable):
    def __init__(self, layer: Layer, group_by: int):
        self.dir = fs.timeline_dir(layer.dir)
        self.group_by = group_by
        self.init = False
        self.interval = self.load_interval(0)
        self.movement_count = 0

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

    def load_interval(self, interval_start_time: int):
        interval_file = fs.interval(self.dir, interval_start_time)
        if fs.base.file_exists(interval_file):
            return self.load_existing_interval(interval_file)
        else:
            return Interval(interval_start_time, self.group_by)

    def time_to_interval_start(self, start_time):
        interval_start_time = (start_time // self.group_by) * self.group_by
        return interval_start_time

    def export_interval(self):
        interval_file = fs.interval(self.dir, self.interval.start_time)
        data = self.interval.serialize()
        fs.base.write_json(interval_file, data)

    def activate_interval(self, start_time: int):
        interval_start_time = self.time_to_interval_start(start_time)
        if self.interval.start_time != interval_start_time:
            self.export_interval()
            self.interval = self.load_interval(interval_start_time)
        

    def add(self, oid: int, model: BaseModel):
        if model.type != "timepoint":
            return
        s, e = self.affected_intervals(model)
        for i in range(s, e + self.group_by, self.group_by):
            self.activate_interval(i)
            self.movement_count += self.interval.insert(model, oid)

    def persist(self):
        self.export_interval()

    def affected_intervals(self, model):
        trip_start = model.start_time
        trip_end = model.end_time - 1
        start_interval = self.time_to_interval_start(trip_start)
        end_interval = self.time_to_interval_start(trip_end) 

        if start_interval > end_interval:
            end_interval = start_interval
        return start_interval, end_interval


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


def build_timeline(layer: Layer):
    secs_in_hour = 60 * 60
    timeline = Timeline(layer, secs_in_hour)
    timeline.clear()

    for oid, object in enumerate(layer.objects):
        for model in object.models:
            timeline.add(oid, model)

    timeline.persist()
    return timeline
