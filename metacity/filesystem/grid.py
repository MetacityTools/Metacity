import os
import shutil
from metacity.filesystem import base


def grid_config(grid_dir):
    return os.path.join(grid_dir, 'grid.json')


def grid_tiles_dir(grid_dir):
    return os.path.join(grid_dir, base.GRID_TILES)


def grid_cache_dir(grid_dir):
    return os.path.join(grid_dir, base.GRID_CACHE)


def tile_dir(grid_dir, tile_name):
    return os.path.join(grid_tiles_dir(grid_dir), tile_name)


def tile_cache_dir(grid_dir, tile_name):
    return os.path.join(grid_cache_dir(grid_dir), tile_name)


def tile_config(grid_dir, tile_name):
    return os.path.join(tile_dir(grid_dir, tile_name), 'config.json')


def tile_names(grid_dir):
    for tile in os.listdir(grid_tiles_dir(grid_dir)):
        yield tile


def recreate_tile(grid_dir, tile_name):
    tile_base = tile_dir(grid_dir, tile_name)
    base.recreate_dir(tile_base)


def recreate_tile_cache(grid_dir, tile_name):
    cache_base = tile_cache_dir(grid_dir, tile_name)
    base.recreate_dir(cache_base)


def recreate_cache(grid_dir):
    for tile in tile_names(grid_dir):
        recreate_tile_cache(grid_dir, tile)


def clear_grid(grid_dir):
    shutil.rmtree(grid_dir)
    os.mkdir(grid_dir)
    os.mkdir(grid_tiles_dir(grid_dir))
    os.mkdir(grid_cache_dir(grid_dir))


def tile_cache_objects(grid_dir, tile_name):
    cache_dir = tile_cache_dir(grid_dir, tile_name)
    return base.objects(cache_dir)


def tile_cache_object_dir(grid_dir, tile_name, oid):
    cache_dir = tile_cache_dir(grid_dir, tile_name)
    return os.path.join(cache_dir, oid)


def tile_cache_object_exists(grid_dir, tile_name, oid):
    dir = tile_cache_object_dir(grid_dir, tile_name, oid)
    return os.path.exists(dir)


def tile_name(x, y):
    return f'{x}_{y}'


def grid_dir(layer_dir):
    return os.path.join(layer_dir, base.GRID)
