from metacity.datamodel.models.set import ModelSet
from metacity.utils.sorter import GridSorter
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.datamodel.grid.grid import RegularGrid
from metacity.datamodel.grid.config import RegularGridConfig
from metacity.datamodel.models.tile import MetaTile
from metacity.filesystem import grid as fs
from metacity.datamodel.object import MetacityObject
from typing import Dict, Iterable
import numpy as np
from tqdm import tqdm


#assemble tiles
def build_tiles(grid: RegularGrid):
    pass



#generate cache
def build_cache(grid: RegularGrid, objects: Iterable[MetacityObject]):
    x_planes, y_planes = grid.splitting_planes()
    sorter = GridSorter(x_planes, y_planes)
    obj: MetacityObject
    for obj in tqdm(objects):
        splitted = obj.models.split(x_planes, y_planes)
        object_into_cache(grid, sorter, obj, splitted)


def object_into_cache(grid, sorter, obj, splitted):
    msets: Dict[(int, int), ModelSet] = {}
    for model in splitted.models:
        x, y = sorter.get_point_idx(model.centroid)
        if (x, y) not in msets:
            msets[(x, y)] = ModelSet()
        msets[(x, y)].models.append(model)

    for (x, y), mset in msets.items():
        tile = grid.tile(x, y)
        tile.add_object_to_cache(grid.dir, obj.oid, mset)
            

# generate layout
def tile_bbox(config: RegularGridConfig, x, y):
    tile_base = [config.x_tile_base(x), config.y_tile_base(y), config.bbox[0, 2]]
    tile_top = [config.x_tile_top(x), config.y_tile_top(y), config.bbox[1, 2]]
    tile_bbox = np.array([tile_base, tile_top])
    return tile_bbox


def init_tile(x, y, bbox, grid_dir):
    tile = MetaTile()
    tile.x, tile.y, tile.tile_bbox = x, y, bbox
    fs.recreate_tile(grid_dir, fs.tile_name(x, y))
    tile.export(grid_dir)


def generate_tiles(config: RegularGridConfig, grid_dir):
    for x in range(config.resolution[0]):
        for y in range(config.resolution[1]):
            bbox = tile_bbox(config, x, y)
            init_tile(x, y, bbox, grid_dir)


def resolution(bbox, tile_size):
    model_range = bbox[1] - bbox[0]
    return np.ceil(model_range[:2] / tile_size).astype(int)


def generate_config(grid: RegularGrid, bbox, tile_size):
    config = grid.config
    config.bbox = bbox
    config.tile_size = tile_size
    config.resolution = resolution(bbox, tile_size)
    print(config.serialize())
    return config


def generate_layout(grid: RegularGrid, bbox, tile_size):
    fs.clear_grid(grid.dir)
    config = generate_config(grid, bbox, tile_size)
    generate_tiles(config, grid.dir)
    config.export()


# main
def build_grid(layer: MetacityLayer, tile_size):
    grid = RegularGrid(layer.dir)
    generate_layout(grid, layer.bbox, tile_size)
    build_cache(grid, layer.objects)
    build_tiles(grid)
    return grid
