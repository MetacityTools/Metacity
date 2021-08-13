import numpy as np
from tqdm import tqdm
from metacity.grid.cache import RegularGridCache
from metacity.grid.config import RegularGridConfig
from metacity.grid.grid import RegularGrid
from metacity.grid.slicer import RegularGridSlicer
from metacity.grid.tile import MetaTile
from metacity.helpers.dirtree import LayerDirectoryTree
from metacity.models.object import MetacityObject
from metacity.project import MetacityLayer


def cache_object(slicer: RegularGridSlicer, cacher: RegularGridCache, object: MetacityObject):
    slicer.slice_object(object)
    cacher.cache_object(object)
    

def build_grid_cache(layer: MetacityLayer, config: RegularGridConfig):
    slicer = RegularGridSlicer(config)
    cacher = RegularGridCache(config, layer.dirtree)
    cacher.clear_cache()
    for obj in tqdm(layer.objects):
        cache_object(slicer, cacher, obj)


def tile_bbox(config: RegularGridConfig, x, y):
    tile_base = [ config.x_tile_base(x), config.y_tile_base(y), config.bbox[0, 2] ]
    tile_top = [ config.x_tile_top(x), config.y_tile_top(y), config.bbox[1, 2] ]
    tile_bbox = np.array([tile_base, tile_top])
    return tile_bbox


def init_tile(dirtree: LayerDirectoryTree, config, x, y):
    bbox = tile_bbox(config, x, y)
    tile = MetaTile()
    tile.x, tile.y, tile.bbox = x, y, bbox
    dirtree.recreate_tile(tile.x, tile.y)
    tile.export(dirtree)


def generate_tiles(dirtree: LayerDirectoryTree, config: RegularGridConfig):
    for x in range(config.resolution[0]):
        for y in range(config.resolution[1]):
            init_tile(dirtree, config, x, y)


def set_resolution(config: RegularGridConfig):
    model_range = config.bbox[1] - config.bbox[0]
    config.resolution = np.ceil(model_range[:2] / config.tile_size).astype(int)


def generate_layout(dirtree: LayerDirectoryTree, config: RegularGridConfig):
    set_resolution(config)
    generate_tiles(dirtree, config)


def build_from_cache(layer: MetacityLayer, config: RegularGridConfig):
    grid = RegularGrid(layer.dirtree)
    tile: MetaTile
    for tile in tqdm(grid.tiles):
        tile.build_from_cache(layer.dirtree, config)        


def build_grid(layer: MetacityLayer, tile_size):
    config = RegularGridConfig(layer.dirtree)
    config.bbox = layer.bbox
    config.tile_size = tile_size
    layer.dirtree.clear_grid()
    generate_layout(layer.dirtree, config)
    config.export(layer.dirtree)
    build_grid_cache(layer, config)
    build_from_cache(layer, config)
    


