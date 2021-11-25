from typing import Callable, Dict
from metacity.datamodel.object import Object, desermodel
from metacity.filesystem import layer as fs
from metacity.geometry import (MultiPoint, MultiLine, MultiPolygon, BaseModel,
                               SegmentCloud, PointCloud, TriangularMesh, MultiTimePoint)
from metacity.utils.persistable import Persistable


class DataSet(Persistable):
    def __init__(self, set_dir: str, offset: int, capacity: int):
        self.set_dir = set_dir
        fs.base.create_dir_if_not_exists(set_dir)
        self.path = fs.data_set(self.set_dir, offset)

        super().__init__(self.path)

        self.offset: int = offset
        self.capacity: int = capacity
        self.data = []

        try:
            self.load()
        except FileNotFoundError:
            self.export()

    @property
    def full(self):
        return self.capacity <= len(self.data)

    def contains(self, index: int):
        return index >= self.offset and index < self.offset + len(self.data)

    def can_contain(self, index: int):
        return (index >= self.offset) and (index < (self.offset + self.capacity))

    def add(self, item):
        self.data.append(item)

    def __getitem__(self, index: int):
        if not self.contains(index):
            raise IndexError(f"No object at index {index}")
        return self.data[index - self.offset]

    def serialize(self):
        return {
            'capacity': self.capacity,
            'offset': self.offset,
        }

    def deserialize(self, data):
        self.capacity = data['capacity']
        self.offset = data['offset']


types: Dict[str, Callable[[], BaseModel]] = {
    MultiPoint().type: MultiPoint,
    PointCloud().type: PointCloud,
    MultiLine().type: MultiLine,
    SegmentCloud().type: SegmentCloud,
    MultiPolygon().type: MultiPolygon,
    TriangularMesh().type: TriangularMesh,
    MultiTimePoint().type: MultiTimePoint
}


def desermodel(model):
    type = model["type"]
    if model["type"] in types:
        m = types[type]()
    else:
        raise RuntimeError(f"Unknown model type: {type}")
    m.deserialize(model)
    return m


class ModelSet(DataSet):
    def __init__(self, layer_dir: str, offset: int, capacity: int):        
        super().__init__(fs.layer_models(layer_dir), offset, capacity)

    def serialize(self): 
        model: BaseModel
        data = super().serialize()
        objects = []
        for object in self.data:
            models = []
            for model in object:
                models.append(model.serialize())
            objects.append(models)
        data['models'] = objects
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.data = []
        for object in data['models']:
            models = []
            for model in object:
                models.append(desermodel(model))
            self.data.append(models)


class MetaSet(DataSet):
    def __init__(self, layer_dir: str, offset: int, capacity: int):        
        super().__init__(fs.layer_metadata(layer_dir), offset, capacity)

    def serialize(self): 
        data = super().serialize()
        data['meta'] = self.data
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.data = data['meta']


class ObjectSet:
    def __init__(self, layer_dir: str, offset: int, capacity: int, load_meta=True, load_model=True):  
        self.readonly = not (load_meta and load_model)
        if not (load_meta or load_model):
            raise Exception("Cannot instantiate ObjectSet without any models or meta")

        self.load_meta = load_meta
        self.load_model = load_model

        if load_model: 
            self.models = ModelSet(layer_dir, offset, capacity)
        if load_meta:
            self.meta = MetaSet(layer_dir, offset, capacity)

    def can_contain(self, index: int):
        if self.load_model:
            return self.models.can_contain(index) 
        return self.meta.can_contain(index) 

    def add(self, object: Object):
        if not self.readonly:
            self.models.add(object.models)
            self.meta.add(object.meta)
        else:
            raise Exception("Cannot object to ObjectSet in readonly mode")

    def __getitem__(self, index: int):
        if self.load_model: 
            if not self.models.contains(index):
                raise IndexError(f"No object at index {index}")
        elif self.load_meta:
            if not self.meta.contains(index):
                raise IndexError(f"No object at index {index}")
        else: 
            raise Exception("Cannot instantiate ObjectSet without any models or meta")
            
        obj = Object()
        if self.load_model: 
            obj.models = self.models[index]
        if self.load_meta:
            obj.meta = self.meta[index] 
        return obj

    def export(self):
        if not self.readonly:
            self.models.export()
            self.meta.export()

