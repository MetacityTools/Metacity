from typing import List
from metacity.datamodel.object import Object
from metacity.filesystem import layer as fs
from metacity.utils.persistable import Persistable


class ObjectSet(Persistable):
    def __init__(self, layer_dir: str, offset: int, capacity: int):
        self.path_geometry = fs.layer_object_set_model(layer_dir, offset)
        self.path_meta = fs.layer_object_set_meta(layer_dir, offset)
        
        super().__init__([self.path_geometry, self.path_meta])
        
        self.offset = offset
        self.capacity = capacity
        self.objects: List[Object] = []
        
        try:
            self.load()
        except IOError:
            self.export()

    @property
    def full(self):
        return self.capacity <= len(self.objects)

    def contains(self, index: int):
        return index >= self.offset and index < self.offset + len(self.objects)

    def can_contain(self, index: int):
        return index >= self.offset and index < self.offset + self.capacity

    def add(self, object: Object):
        self.objects.append(object)

    def __getitem__(self, index: int):
        if not self.contains(index):
            raise IndexError(f"No object at index {index}")
        return self.objects[index - self.offset]

    def serialize(self): 
        models = []
        meta = []
        for object in self.objects:
            o = object.serialize()
            models.append(o['models'])
            meta.append(o['meta'])

        return {
                'type': 'models',
                'models': models
            }, {
                'type': 'meta',
                'meta': meta,
                'capacity': self.capacity,
                'offset': self.offset
            }

    def deserialize(self, models, meta):
        self.objects = []

        for g, m in zip(models['models'], meta['meta']):
            o = Object()
            o.deserialize(g, m)
            self.objects.append(o)

        self.capacity = meta['capacity']
        self.offset = meta['offset']



