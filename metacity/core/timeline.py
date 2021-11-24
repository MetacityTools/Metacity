from metacity.datamodel.layer import Layer
import metacity.filesystem.timeline as fs
from metacity.geometry import BaseModel
from metacity.utils.persistable import Persistable


class Timeline(Persistable):
    def __init__(self, layer_dir: str, group_by: int):
        self.dir = fs.timeline_dir(layer_dir)
        self.group_by = group_by
        self.init = False

        super().__init__(fs.timeline_config(self.dir))

        try:
            self.load()
        except FileNotFoundError:
            pass

    def clear(self):
        fs.clear_timeline(self.dir)

    def add(self, oid: int, model: BaseModel):
        if model.type != "timepoint":
            return

        #TODO
        
        

    def serialize(self):
        return {
            "group_by": self.group_by,
            "init": self.init
        }

    def deserialize(self, data):
        self.group_by = data["group_by"]
        self.init = data["init"]


def build_timeline(layer: Layer):
    secs_in_hour = 60 * 60
    timeline = Timeline(layer.dir, secs_in_hour)
    timeline.clear()

    for oid, object in enumerate(layer.objects):
        for model in object.models:
            timeline.add(oid, model)
            
    return timeline
