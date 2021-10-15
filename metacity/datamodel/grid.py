from collections import defaultdict
from typing import DefaultDict, Dict, Tuple

from metacity.datamodel.set import TileSet
from metacity.filesystem import grid as fs
from metacity.filesystem import file as fsf
from metacity.geometry.primitive import Primitive, SimplePrimitive
from metacity.utils.persistable import Persistable


class TileCache:
    def __init__(self, grid_dir: str, name: str):
        self.name = name
        self.grid_dir = grid_dir
        self.size = 0
        self.group_by = 1000
        self.set = TileSet(self.grid_dir, self.name, 0, self.group_by)

    def add(self, oid: int, model: SimplePrimitive):
        if not self.set.can_contain(self.size):
            self.set.export()
            self.activate_set(self.size)
        model.add_attribute("oid", oid)
        self.set.add(model)
        self.size += 1

    def __getitem__(self, index: int):
        if not self.set.can_contain(index):
            self.activate_set(index)
        obj: SimplePrimitive = self.set[index]
        return obj

    def activate_set(self, index):
        offset = (index // self.group_by) * self.group_by
        self.set = TileSet(self.grid_dir, self.name, offset, self.group_by)

    @property
    def models(self):
        for i in range(self.size):
            yield self[i]

    def to_tile(self):
        output = fs.grid_tiles_dir(self.grid_dir)
        aggregate_models : Dict[str, SimplePrimitive] = {}
        
        for model in self.models:
            if model.type not in aggregate_models:
                aggregate_models[model.type] = model.copy()
            else:
                aggregate_models[model.type].join(model)
                
        serialized = [ m.serialize() for m in aggregate_models.values() ]
        fsf.write_json(output, serialized)



class Grid(Persistable):
    def __init__(self, layer_dir: str):
        self.dir = fs.grid_dir(layer_dir)
        super().__init__(fs.grid_config(self.dir))

        self.tile_size = 1000
        gen_tile = lambda x, y: TileCache(self.dir, fs.tile_name(x, y))
        self.cache: DefaultDict[Tuple[int, int], TileCache] = defaultdict(gen_tile)

        try:
            self.load()
        except IOError:
            self.export()

    def clear(self):
        fs.clear_grid(self.dir)

    def add(self, oid: int, model: Primitive):
        submodel = model.transform()
        submodels = submodel.slice_to_grid(self.tile_size)
        for model in submodels:
            xy = self.v_to_xy(model.centroid)
            self.cache[xy].add(oid, model)

    def v_to_xy(self, vertex):
        return (vertex[0] // self.tile_size, vertex[1] // self.tile_size)

    def persist(self):
        for cache in self.cache.values():
            cache.to_tile(self.dir)
        self.export()

    def serialize(self):
        return {
            "tile_size": self.tile_size
        }

    def deserialize(self, data):
        self.tile_size = data["tile_size"]


