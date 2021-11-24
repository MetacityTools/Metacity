from typing import List

from metacity.datamodel.set import DataSet, desermodel
from metacity.filesystem import grid as gfs
from metacity.filesystem import layer as fs
from metacity.filesystem.base import read_json
from metacity.geometry import Model


class TileSet(DataSet):
    def __init__(self, grid_dir: str, tile_name: str, offset: int, capacity: int):        
        super().__init__(gfs.grid_cache_tile_dir(grid_dir, tile_name), offset, capacity)

    def serialize(self): 
        data = super().serialize()
        models = []
        model: Model
        for model in self.data:
            models.append(model.serialize())
        data['models'] = models
        return data

    def deserialize(self, data):
        super().deserialize(data)
        self.data = []
        for model in data['models']:
            self.data.append(desermodel(model))


class Tile:
    def __init__(self, tile_file):
        self.file = tile_file
        self.x, self.y = gfs.tile_xy(fs.base.filename(tile_file))
        self.models: List[Model] = []
        for model in read_json(self.file):
            self.models.append(desermodel(model))

    #this should get refactored out later
    @property
    def polygon(self):
        for m in self.models:
            if m.type == "simplepolygon":
                return m
        return None

    @property
    def name(self):
        return gfs.tile_name(self.x, self.y)

