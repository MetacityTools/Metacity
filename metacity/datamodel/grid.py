from collections import defaultdict
from typing import DefaultDict, Tuple

from metacity.datamodel.set import TileSet
from metacity.filesystem import grid as fs
from metacity.geometry.primitive import Primitive
from metacity.utils.persistable import Persistable


class Tile:
    def __init__(self, grid_dir: str, name: str):
        self.name = name
        self.grid_dir = grid_dir
        self.size = 0
        self.group_by = 1000
        self.set = TileSet(self.grid_dir, self.name, 0, self.group_by)

    def add(self, oid: int, model: Primitive):
        if not self.set.can_contain(self.size):
            self.set.export()
            self.activate_set(self.size)
        self.set.add(oid, model)
        self.size += 1

    def __getitem__(self, index: int):
        if not self.set.can_contain(index):
            self.activate_set(index)
        obj = self.set[index]
        return obj

    def activate_set(self, index):
        offset = (index // self.group_by) * self.group_by
        self.set = TileSet(self.grid_dir, self.name, offset, self.group_by)

    @property
    def models(self):
        for i in range(self.size):
            yield self[i]


class Grid(Persistable):
    def __init__(self, layer_dir: str):
        self.dir = fs.grid_dir(layer_dir)
        super().__init__(fs.grid_config(self.dir))

        self.tile_size = 1000
        self.size = 0
        gen_tile = lambda x, y: Tile(self.dir, fs.tile_name(x, y))
        self.tiles: DefaultDict[Tuple[int, int], Tile] = defaultdict(gen_tile)

        try:
            self.load()
        except IOError:
            self.export()

    def clear(self):
        fs.clear_grid(self.dir)

    def add(self, oid: int, model: Primitive):
        submodels = model.slice_to_grid(self.tile_size)
        for model in submodels:
            xy = self.v_to_xy(model.centroid)
            self.tiles[xy].add(oid, model)

    def v_to_xy(self, vertex):
        return (vertex[0] // self.tile_size, vertex[1] // self.tile_size)

    def serialize(self):
        for tile in self.tiles.values():
            tile.persist()
            #TODO

        return {
            "tile_size": self.tile_size,
            "size": self.size
        }

    def deserialize(self, data):
        self.tile_size = data["tile_size"]
        self.size = data["size"]

        for tile in fs.grid_tiles(self.dir):
            t = Tile(self.dir)
            #TODO
