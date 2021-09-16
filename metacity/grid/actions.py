from metacity.datamodel.object import MetacityObject
from metacity.grid.build import build_grid, build_cache, build_tiles
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.datamodel.grid.grid import RegularGrid


def delete_object(grid: RegularGrid, oid: str):
    for tile in grid.tiles:
        tile.delete_object_from_cache(grid.dir, oid)


def rebuild_grid(layer: MetacityLayer, tile_size=None):
    if tile_size is None:
        grid = RegularGrid(layer.dir)
        tile_size = grid.config.tile_size
    build_grid(layer, tile_size) 


def add_object(grid: RegularGrid, object: MetacityObject):
    tiles = build_cache(grid, [object])
    build_tiles(grid, tiles)
