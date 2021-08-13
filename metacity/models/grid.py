from metacity.models.tiles.object import MetaTile
from metacity.grid.config import RegularGridConfig
from metacity.grid.slicer import RegularGridSlicer
from metacity.grid.cache import RegularGridCache

from helpers.dirtree import grid as tree


class RegularGrid:
    def __init__(self, layer_dir):
        self.dir = layer_dir


    @property
    def config(self):
        return RegularGridConfig(self.dir)


    @property
    def slicer(self):
        return RegularGridSlicer(self.dir)


    @property
    def cache(self):
        return RegularGridCache(self.dir)


    @property
    def tiles(self):
        tile_name: str
        for tile_name in tree.tile_names(self.dir):
            x, y = [ int(i) for i in tile_name.split("_") ]
            tile = MetaTile()
            tile.load(x, y, self.dir)
            yield tile

