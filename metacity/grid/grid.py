from metacity.grid.tile import MetaTile
from metacity.grid.config import RegularGridConfig
from metacity.grid.slicer import RegularGridSlicer
from metacity.grid.cache import RegularGridCache


class RegularGrid:
    def __init__(self, dirtree):
        self.dirtree = dirtree


    @property
    def config(self):
        return RegularGridConfig(self.dirtree)


    @property
    def slicer(self):
        return RegularGridSlicer(self.config)


    @property
    def cache(self):
        return RegularGridCache(self.cofig, self.dirtree)


    @property
    def tiles(self):
        tile_name: str
        for tile_name in self.dirtree.tile_names:
            x, y = [ int(i) for i in tile_name.split("_") ]
            tile = MetaTile()
            tile.load(x, y, self.dirtree)
            yield tile

