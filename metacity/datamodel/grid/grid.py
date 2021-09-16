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

    def tile(self, x, y):
        tile = MetaTile()
        tile.load(self.dir, fs.tile_name(x, y))
        return tile

    def splitting_planes(self):
        resolution = self.config.resolution
        x_planes = []
        for x in range(resolution[0] - 1):
            x_planes.append(self.config.x_tile_top(x))
        y_planes = []
        for y in range(resolution[1] - 1):
            y_planes.append(self.config.y_tile_top(y))
        return x_planes, y_planes
