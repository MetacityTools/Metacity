import os
import shutil
from metacity.helpers.dirtree import base


def grid_config(layer_dir):
    return os.path.join(layer_dir, base.GRID, 'grid.json')


def tile_dir(layer_dir, tile_name):
    return os.path.join(layer_dir, base.GRID_TILES, tile_name)


def tile_cache_dir(layer_dir, tile_name):
    return os.path.join(layer_dir, base.GRID_CACHE, tile_name)


def tile_config(layer_dir, tile_name):
    return os.path.join(layer_dir, base.GRID_TILES, tile_name, 'config.json')


def tile_names(layer_dir):
    grid_base = os.path.join(layer_dir, base.GRID_TILES)
    for tile in os.listdir(grid_base):
        yield tile


def recreate_tile(layer_dir, tile_name):
    tile_base = tile_dir(layer_dir, tile_name)
    base.recreate_dir(tile_base)
    base.recreate_lod_dirs(tile_base)


def recreate_tile_cache(layer_dir, tile_name):
    cache_base = tile_cache_dir(layer_dir, tile_name)
    base.recreate_dir(cache_base)
    base.recreate_geometry_tree(cache_base)


def recreate_cache(layer_dir):
    for tile in tile_names(layer_dir):
        recreate_tile_cache(layer_dir, tile)


def clear_grid(layer_dir):
    grid = os.path.join(layer_dir, base.GRID)
    shutil.rmtree(grid)
    os.mkdir(grid)
    os.mkdir(os.path.join(layer_dir, base.GRID_CACHE))
    os.mkdir(os.path.join(layer_dir, base.GRID_TILES))


def tile_cache_objects(layer_dir, tile_name):
    cache_dir = tile_cache_dir(layer_dir, tile_name)
    return base.objects(cache_dir)


def tile_name(x, y):
    return f'{x}_{y}'


def path_to_tile_lod(tile_dir, primitive, lod):
    return os.path.join(tile_dir, str(lod), primitive + '.json')

