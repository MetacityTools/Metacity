from metacity.datamodel.layer.layer import MetacityLayer
from metacity.datamodel.grid.grid import RegularGrid
from metacity.filesystem import grid as fs


def generate_layout(grid: RegularGrid, bbox, tile_size):
    fs.clear_grid(grid.dir)
    pass


# main
def build_grid(layer: MetacityLayer, tile_size):
    grid = RegularGrid(layer.dir)
    generate_layout(grid, layer.bbox, tile_size)




