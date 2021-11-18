import os
import shutil
from metacity.filesystem import base


def grid_config(grid_dir):
    return os.path.join(grid_dir, 'grid.json')


def grid_tiles_dir(grid_dir):
    return os.path.join(grid_dir, base.GRID_TILES)


def grid_cache_dir(grid_dir):
    return os.path.join(grid_dir, base.GRID_CACHE)


def grid_stream_dir(grid_dir):
    return os.path.join(grid_dir, base.GRID_STREAM)


def grid_cache_tile_dir(grid_dir, tile_name):
    return os.path.join(grid_cache_dir(grid_dir), tile_name)


def clear_grid(grid_dir):
    shutil.rmtree(grid_dir)
    os.mkdir(grid_dir)
    os.mkdir(grid_tiles_dir(grid_dir))
    os.mkdir(grid_stream_dir(grid_dir))
    os.mkdir(grid_cache_dir(grid_dir))


def tile_cache_tile_set(grid_dir, tile_name, offset):
    cache_dir = grid_cache_tile_dir(grid_dir, tile_name)
    return os.path.join(cache_dir, f"set{offset}.json")


def grid_tile(grid_dir, tile_name):
    tiles_dir = grid_tiles_dir(grid_dir)
    return os.path.join(tiles_dir, f"{tile_name}.json")


def grid_stream(grid_dir, tile_name):
    tiles_dir = grid_stream_dir(grid_dir)
    return os.path.join(tiles_dir, f"{tile_name}.json")


def tile_name(x: int, y: int):
    return f'tile{x}_{y}'


def tile_xy(name: str):
    return [int(i) for i in name[4:-5].split("_")]


def grid_dir(layer_dir):
    return os.path.join(layer_dir, base.GRID)


def grid_tiles(grid_dir):
    tile_dir = grid_tiles_dir(grid_dir)
    for tile in os.listdir(tile_dir):
        yield os.path.join(tile_dir, tile)