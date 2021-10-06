from metacity.datamodel.object import Object
from metacity.grid.build import build_grid, build_cache, build_tiles
from metacity.datamodel.layer.layer import Layer
from metacity.datamodel.grid.grid import RegularGrid


def delete_object(grid: RegularGrid, oid: str):
    tiles = []
    for tile in grid.tiles:
        if tile.contains_object(grid.dir, oid):
            tile.delete_object_from_cache(grid.dir, oid)
            tiles.append(tile)
    build_tiles(grid, tiles)


def rebuild_grid(layer: Layer, tile_size=None):
    if tile_size is None:
        grid = RegularGrid(layer.dir)
        tile_size = grid.config.tile_size
    build_grid(layer, tile_size) 


def add_object(grid: RegularGrid, object: Object):
    tile_ids = build_cache(grid, [object])
    build_tiles(grid, tile_ids)
