from typing import Callable, Dict, List
from metacity.datamodel.object import Object, desermodel
from metacity.filesystem import layer as fs
from metacity.filesystem import grid as gfs
from metacity.geometry import (MultiPoint, MultiLine, MultiPolygon, Primitive, SimplePrimitive,
                               SimpleMultiLine, SimpleMultiPoint, SimpleMultiPolygon)
from metacity.filesystem.base import read_json
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


types: Dict[str, Callable[[],Primitive]] = {
    MultiPoint().type: MultiPoint,
    SimpleMultiPoint().type: SimpleMultiPoint,
    MultiLine().type: MultiLine,
    SimpleMultiLine().type: SimpleMultiLine,
    MultiPolygon().type: MultiPolygon,
    SimpleMultiPolygon().type: SimpleMultiPolygon,
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
        model: Primitive
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


class TileSet(DataSet):
    def __init__(self, grid_dir: str, tile_name: str, offset: int, capacity: int):        
        super().__init__(gfs.grid_cache_tile_dir(grid_dir, tile_name), offset, capacity)

    def serialize(self): 
        data = super().serialize()
        models = []
        model: SimplePrimitive
        for model in self.data:
            models.append(model.serialize())
        data['models'] = models
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.data = []
        for model in data['models']:
            self.data.append(desermodel(model))


def join_boxes(boxes):
    return [[ min([ box[0][i] for box in boxes ]) for i in range(3) ], [ max([ box[1][i] for box in boxes ]) for i in range(3) ]]


class Tile:
    def __init__(self, tile_file):
        self.file = tile_file
        self.x, self.y = gfs.tile_xy(fs.base.filename(tile_file))
        self.objects: List[SimplePrimitive] = []
        for model in read_json(self.file):
            self.objects.append(desermodel(model))

    @property
    def polygon(self):
        for o in self.objects:
            if o.type == "simplepolygon":
                return o
        return None

    @property
    def name(self):
        return gfs.tile_name(self.x, self.y)

    def build_layout(self):
        box = join_boxes([o.bounding_box for o in self.objects])
        return {
            'box': box,
            'x': self.x,
            'y': self.y,
            'file': fs.base.filename(self.file)
        }
