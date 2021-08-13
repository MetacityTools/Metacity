from typing import Iterable
import numpy as np
from metacity.grid.cache import RegularGridCache
from metacity.grid.config import RegularGridConfig
from metacity.grid.slicer import RegularGridSlicer
from metacity.helpers.dirtree import grid as tree
from metacity.helpers.dirtree import layer as ltree
from metacity.models.grid import RegularGrid
from metacity.models.object import MetacityObject
from metacity.models.tiles.object import MetaTile
from metacity.project import MetacityLayer
from tqdm import tqdm


#build from cache
def tile_from_cache(tile: MetaTile, grid: RegularGrid, config: RegularGridConfig):
    cache_path = ltree.layer_cache(grid.dir)
    meta_path = ltree.layer_metadata(grid.dir)

    for oid in tree.tile_cache_objects(grid.dir, tile.name):
        object = MetacityObject()
        object.load(oid, cache_path, meta_path)
        bid = config.id_for_oid(object.oid)
        tile.join_object(object, bid)
        tile.objects += 1

    tile.consolidate()
    tile.export(grid.dir)


def cache_to_tiles(grid: RegularGrid):
    config = grid.config
    for tile in tqdm(grid.tiles):
        tile_from_cache(tile, grid, config)  
    config.export() 


#generate cache
def cache_object(slicer: RegularGridSlicer, cache: RegularGridCache, object: MetacityObject):
    slicer.slice_object(object)
    cache.insert_object(object)
    

def build_cache(grid: RegularGrid, objects: Iterable[MetacityObject]):
    slicer = grid.slicer
    cache = grid.cache
    cache.clear_cache()
    for obj in tqdm(objects):
        cache_object(slicer, cache, obj)   


#generate layout
def tile_bbox(config: RegularGridConfig, x, y):
    tile_base = [ config.x_tile_base(x), config.y_tile_base(y), config.bbox[0, 2] ]
    tile_top = [ config.x_tile_top(x), config.y_tile_top(y), config.bbox[1, 2] ]
    tile_bbox = np.array([tile_base, tile_top])
    return tile_bbox


def init_tile(x, y, bbox, layer_dir):
    tile = MetaTile()
    tile.x, tile.y, tile.bbox = x, y, bbox
    tree.recreate_tile(layer_dir, tree.tile_name(x, y))
    tile.export(layer_dir)


def generate_tiles(config: RegularGridConfig, layer_dir):
    for x in range(config.resolution[0]):
        for y in range(config.resolution[1]):
            bbox = tile_bbox(config, x, y)
            init_tile(x, y, bbox, layer_dir)


def resolution(bbox, tile_size):
    model_range = bbox[1] - bbox[0]
    return np.ceil(model_range[:2] / tile_size).astype(int)


def generate_config(grid: RegularGrid, bbox, tile_size):
    config = grid.config
    config.bbox = bbox
    config.tile_size = tile_size
    config.resolution = resolution(bbox, tile_size)
    return config


def generate_layout(grid: RegularGrid, bbox, tile_size):
    tree.clear_grid(grid.dir)
    config = generate_config(grid, bbox, tile_size)
    generate_tiles(config, grid.dir)
    config.export(grid.dir)


#main
def build_grid(layer: MetacityLayer, tile_size):
    grid = RegularGrid(layer.dir)
    generate_layout(grid, layer.bbox, tile_size)
    build_cache(grid, layer.objects)
    cache_to_tiles(grid)
    return grid
    


