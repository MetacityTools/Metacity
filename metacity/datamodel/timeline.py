import metacity.filesystem.timeline as fs
from metacity.geometry import Primitive
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
            self.export()

    def clear(self):
        fs.clear_timeline(self.dir)

    def add(self, oid: int, model: Primitive):
        pass
        #TODO

    def serialize(self):
        return {
            "group_by": self.group_by,
            "init": self.init
        }

    def deserialize(self, data):
        self.group_by = data["group_by"]
        self.init = data["init"]

