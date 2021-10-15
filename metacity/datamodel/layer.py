from metacity.datamodel.grid import Grid
from metacity.datamodel.object import Object
from metacity.datamodel.set import ObjectSet
from metacity.filesystem import layer as fs
from metacity.utils.bbox import bboxes_bbox
from metacity.utils.persistable import Persistable


class Layer(Persistable):
    def __init__(self, layer_dir: str):
        super().__init__(fs.layer_config(layer_dir))

        self.dir = layer_dir
        self.shift = [0., 0., 0.]
        self.size = 0
        self.group_by = 1000
        self.set = ObjectSet(self.dir, 0, self.group_by)

        fs.create_layer(layer_dir)

        try:
            self.load()
        except IOError:
            self.export()

    @property
    def name(self):
        return fs.layer_name(self.dir)

    def add(self, object: Object):
        if not self.set.can_contain(self.size):
            self.set.export()
            self.activate_set(self.size)
        self.set.add(object)
        self.size += 1

    def persist(self):
        self.export()
        self.set.export()

    def __getitem__(self, index: int):
        if not self.set.can_contain(index):
            self.activate_set(index)
        obj = self.set[index]
        return obj

    def activate_set(self, index):
        offset = (index // self.group_by) * self.group_by
        self.set = ObjectSet(self.dir, offset, self.group_by)

    @property
    def objects(self):
        for i in range(self.size):
            yield self[i]

    def add_source_file(self, source_file_path: str):
        return fs.copy_to_layer(self.dir, source_file_path)

    def build_grid(self):
        grid = Grid(self.dir)
        grid.clear()
        for oid, object in enumerate(self.objects):
            for model in object.models:
                grid.add(oid, model) 

    def serialize(self):
        return {
            'shift': self.shift,
            'size': self.size,
            'group_by': self.group_by
        }

    def deserialize(self, data):
        self.shift = data['shift']
        self.size = data['size']
        self.group_by = data['group_by']