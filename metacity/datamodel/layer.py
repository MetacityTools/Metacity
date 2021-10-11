from metacity.datamodel.object import Object
from metacity.datamodel.set import ObjectSet
from metacity.filesystem import layer as fs
from metacity.utils.bbox import bboxes_bbox
from metacity.datamodel.grid.grid import RegularGrid
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
    def grid(self):
        return RegularGrid(self.dir)

    @property
    def bbox(self):
        return bboxes_bbox([object.models.bbox for object in self.objects])

    @property
    def name(self):
        return fs.layer_name(self.dir)

    def add(self, object: Object):
        if not self.set.can_contain(self.size):
            self.set.export()
            offset = (self.size // self.group_by) * self.group_by
            self.set = ObjectSet(self.dir, offset, self.group_by)
        self.set.add(object)
        self.size += 1

    def persist(self):
        self.export()
        self.set.export()

    def __getitem__(self, index: int):
        if not self.set.can_contain(index):
            offset = (index // self.group_by) * self.group_by
            self.set = ObjectSet(self.dir, offset, self.group_by)
        obj = self.set[index]
        return obj

    @property
    def objects(self):
        for i in range(self.size):
            yield self[i]

    def add_source_file(self, source_file_path: str):
        return fs.copy_to_layer(self.dir, source_file_path)

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