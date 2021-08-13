import numpy as np
from metacity.grid import config
from metacity.grid.cache import RegularGridCache
from metacity.grid.config import RegularGridConfig
from metacity.grid.slicer import RegularGridSlicer
from metacity.helpers.dirtree import grid as tree
from metacity.models.grid import RegularGrid
from metacity.models.object import MetacityObject
from metacity.models.tiles.object import MetaTile
from metacity.project import MetacityLayer
from tqdm import tqdm


#build from cache
def tile_from_cache(tile: MetaTile, layer: MetacityLayer, config: RegularGridConfig):
    cache_path = layer.cache_path
    meta_path = layer.meta_path

    for oid in tree.tile_cache_objects(layer.dir, tile.name):
        object = MetacityObject()
        object.load(oid, cache_path, meta_path)
        bid = config.id_for_oid(object.oid)
        tile.join_object(object, bid)
        tile.objects += 1

    tile.consolidate()
    tile.export(layer.dir)


def build_from_cache(layer: MetacityLayer):
    grid = RegularGrid(layer.dir)
    config = grid.config
    for tile in tqdm(grid.tiles):
        tile_from_cache(tile, layer, config)  
    config.export() 


#generate cache
def cache_object(slicer: RegularGridSlicer, cacher: RegularGridCache, object: MetacityObject):
    slicer.slice_object(object)
    cacher.cache_object(object)
    

def build_grid_cache(layer: MetacityLayer):
    slicer = RegularGridSlicer(layer.dir)
    cacher = RegularGridCache(layer.dir)
    cacher.clear_cache()
    for obj in tqdm(layer.objects):
        cache_object(slicer, cacher, obj)   


#generate layout
def tile_bbox(config: RegularGridConfig, x, y):
    tile_base = [ config.x_tile_base(x), config.y_tile_base(y), config.bbox[0, 2] ]
    tile_top = [ config.x_tile_top(x), config.y_tile_top(y), config.bbox[1, 2] ]
    tile_bbox = np.array([tile_base, tile_top])
    return tile_bbox


def init_tile(layer_dir, config, x, y):
    tile = MetaTile()
    tile.x, tile.y, tile.bbox = x, y, tile_bbox(config, x, y)
    tree.recreate_tile(layer_dir, tree.tile_name(x, y))
    tile.export(layer_dir)


def generate_tiles(config: RegularGridConfig, layer_dir):
    for x in range(config.resolution[0]):
        for y in range(config.resolution[1]):
            init_tile(layer_dir, config, x, y)


def set_resolution(config: RegularGridConfig):
    model_range = config.bbox[1] - config.bbox[0]
    config.resolution = np.ceil(model_range[:2] / config.tile_size).astype(int)


def generate_config(layer, tile_size):
    config = RegularGridConfig(layer.dir)
    config.bbox = layer.bbox
    config.tile_size = tile_size
    set_resolution(config)
    return config


def generate_layout(layer: MetacityLayer, tile_size):
    config = generate_config(layer, tile_size)
    generate_tiles(config, layer.dir)
    config.export(layer.dir)



#main
def build_grid(layer: MetacityLayer, tile_size):
    #TODO refactor more
    tree.clear_grid(layer.dir)
    generate_layout(layer, tile_size)
    build_grid_cache(layer)
    build_from_cache(layer)
    


