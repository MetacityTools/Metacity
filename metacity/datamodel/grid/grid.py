from metacity.filesystem import grid as fs
from metacity.datamodel.grid.config import RegularGridConfig
from metacity.datamodel.models.tile import MetaTile

class RegularGrid:
    def __init__(self, layer_dir):
        self.dir = fs.grid_dir(layer_dir)

    @property
    def config(self):
        return RegularGridConfig(self)

    @property
    def tiles(self):
        for tile_name in fs.tile_names(self.dir):
            tile = MetaTile()
            tile.load(self.dir, tile_name)
            yield tile
