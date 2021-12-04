from typing import Dict, Tuple, Union
from metacity.datamodel.layer import Layer, LayerOverlay

from metacity.core.grid.set import TileSet, Tile
from metacity.filesystem import grid as fs
from metacity.geometry import BaseModel, Model
from metacity.utils.persistable import Persistable


class TileCache:
    def __init__(self, grid_dir: str, name: str, group_by=1000):
        self.name = name
        self.grid_dir = grid_dir
        self.size = 0
        self.group_by = group_by
        self.set = TileSet(self.grid_dir, self.name, 0, self.group_by)

    def add(self, oid: int, model: Model):
        if not self.set.can_contain(self.size):
            self.set.export()
            self.activate_set(self.size)
        model.add_attribute("oid", oid)
        self.set.add(model)
        self.size += 1

    def __getitem__(self, index: int):
        if not self.set.can_contain(index):
            self.set.export()
            self.activate_set(index)
        obj: Model = self.set[index]
        return obj

    def activate_set(self, index):
        offset = (index // self.group_by) * self.group_by
        self.set = TileSet(self.grid_dir, self.name, offset, self.group_by)

    @property
    def models(self):
        for i in range(self.size):
            yield self[i]

    def to_tile(self):
        output = fs.grid_tile(self.grid_dir, self.name)
        output_stream = fs.grid_stream(self.grid_dir, self.name)
        aggregate_models : Dict[str, Model] = {}
        
        for model in self.models:
            if model.type not in aggregate_models:
                aggregate_models[model.type] = model.copy()
            else:
                aggregate_models[model.type].join(model)
                
        serialized = [m.serialize() for m in aggregate_models.values()]
        fs.base.write_json(output, serialized)
        serialized = [m.serialize_stream() for m in aggregate_models.values()]
        fs.base.write_json(output_stream, serialized)

    @staticmethod
    def is_valid(grid_dir, tile_name):
        dir = fs.grid_cache_tile_dir(grid_dir, tile_name)
        return fs.base.is_path_exists_or_creatable(dir)


class Grid(Persistable):
    def __init__(self, layer: Union[Layer, LayerOverlay]):
        self.dir = fs.grid_dir(layer.dir)
        super().__init__(fs.grid_config(self.dir))

        self.tile_size = 1000
        self.init = False
        self.cache: Dict[Tuple[int, int], TileCache] = {}

        try:
            self.load()
        except FileNotFoundError:
            pass

    def clear(self):
        fs.clear_grid(self.dir)

    def add(self, oid: int, model: BaseModel):
        submodel = model.transform()
        if submodel is None:
            return
             
        submodels = submodel.slice_to_grid(self.tile_size)
        for model in submodels:
            x, y = self.v_to_xy(model.centroid)
            name = fs.tile_name(x, y)

            if not TileCache.is_valid(self.dir, name):
                continue

            if (x, y) not in self.cache:
                self.cache[x, y] = TileCache(self.dir, name)
            self.cache[x, y].add(oid, model)

    def v_to_xy(self, vertex):
        return (int(vertex[0] // self.tile_size), int(vertex[1] // self.tile_size))

    def persist(self, progressCallback=None):
        for cache in self.cache.values():
            cache.to_tile()
            if progressCallback is not None:
                progressCallback(f"cache {cache.name}")

        self.init = True
        self.export()

    @property
    def tiles(self):
        for tile in fs.grid_tiles(self.dir):
            yield Tile(tile)

    def __getitem__(self, xy):
        path = fs.grid_tile(self.dir, fs.tile_name(*xy))
        if fs.base.file_exists(path):
            return Tile(path)
        return None

    def overlay(self, grid):
        for tile_path in fs.grid_tiles(self.dir):
            xy = fs.tile_xy(fs.base.filename(tile_path))
            tile: Tile = grid[xy]
            if tile is not None:
                yield Tile(tile_path), tile

    def tile_from_single_model(self, model: Model, tile_name):
        output = fs.grid_tile(self.dir, tile_name)
        fs.base.write_json(output, [model.serialize()])
        output_stream = fs.grid_stream(self.dir, tile_name)
        fs.base.write_json(output_stream, [model.serialize_stream()])   

    def rebuild_stream_data(self):
        for tile in self.tiles:
            output_stream = fs.grid_stream(self.dir, tile.name)
            fs.base.write_json(output_stream, [model.serialize_stream() for model in tile.models])         

    def serialize(self):
        return {
            "tile_size": self.tile_size,
            "init": self.init
        }

    def deserialize(self, data):
        self.tile_size = data["tile_size"]
        self.init = data["init"]


def build_grid(layer: Layer, progressCallback=None):
    grid = Grid(layer)
    grid.clear()
    for oid, object in enumerate(layer.objects):
        for model in object.models:
            grid.add(oid, model) 
    grid.persist(progressCallback)
    return grid