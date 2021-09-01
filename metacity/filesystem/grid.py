import os
import shutil
from metacity.filesystem import base


def grid_config(grid_dir):
    return os.path.join(grid_dir, 'grid.json')


def tile_dir(grid_dir, tile_name):
    return os.path.join(grid_dir, base.GRID_TILES, tile_name)


def tile_cache_dir(grid_dir, tile_name):
    return os.path.join(grid_dir, base.GRID_CACHE, tile_name)


def tile_model_dir(grid_dir, tile_name):
    return os.path.join(tile_dir(grid_dir, tile_name), base.TILE_MODLES)


def tile_config(grid_dir, tile_name):
    return os.path.join(tile_dir(grid_dir, tile_name), 'config.json')


def tile_names(grid_dir):
    grid_base = os.path.join(grid_dir, base.GRID_TILES)
    for tile in os.listdir(grid_base):
        yield tile


def recreate_tile(grid_dir, tile_name):
    tile_base = tile_dir(grid_dir, tile_name)
    base.recreate_dir(tile_base)
    base.recreate_dir(os.path.join(tile_base, base.TILE_MODLES))


def recreate_tile_cache(grid_dir, tile_name):
    cache_base = tile_cache_dir(grid_dir, tile_name)
    base.recreate_dir(cache_base)


def recreate_cache(grid_dir):
    for tile in tile_names(grid_dir):
        recreate_tile_cache(grid_dir, tile)


def clear_grid(grid_dir):
    shutil.rmtree(grid_dir)
    os.mkdir(grid_dir)
    os.mkdir(os.path.join(grid_dir, base.GRID_CACHE))
    os.mkdir(os.path.join(grid_dir, base.GRID_TILES))


def tile_cache_objects(grid_dir, tile_name):
    cache_dir = tile_cache_dir(grid_dir, tile_name)
    return base.objects(cache_dir)


def tile_objects(grid_dir, tile_name):
    model_dir = tile_model_dir(grid_dir, tile_name)
    return base.objects(model_dir)


def tile_name(x, y):
    return f'{x}_{y}'


def grid_dir(layer_dir):
    return os.path.join(layer_dir, base.GRID)
