from sys import meta_path
from typing import Dict
import numpy as np
from metacity.grid.config import RegularGridConfig
from metacity.models.object import MetacityObject, ObjectLODs
from metacity.helpers.dirtree import grid as tree


def copy_lod_semantics(original: ObjectLODs, copy: ObjectLODs):
    for lod in range(0, 5):
        copy.lod[lod].semantics_meta = original.lod[lod].semantics_meta


def copy_semantics(object, cache_obj):
    copy_lod_semantics(object.facets, cache_obj.facets)
    copy_lod_semantics(object.lines, cache_obj.lines)
    copy_lod_semantics(object.points, cache_obj.points)


def create_cache_obj(object: MetacityObject, tile: Dict[str, MetacityObject]):
    cache_obj = MetacityObject()
    cache_obj.oid = object.oid
    cache_obj.meta = object.meta
    copy_semantics(object, cache_obj)
    tile[object.oid] = cache_obj
    return cache_obj



class InMemoryCache:
    def __init__(self, layer_dir):
        self.tiles = {}
        self.config = RegularGridConfig(layer_dir)


    def clear(self):
        self.tiles = {}


    def get_object(self, x, y, object: MetacityObject):
        if (x, y) not in self.tiles:
            self.tiles[(x, y)] = {}
        tile = self.tiles[(x, y)]
        if object.oid not in tile:
            return create_cache_obj(object, tile)
        return tile[object.oid]


    def triangle_tile_index(self, triangle):
        center = np.sum(triangle, axis=0) / 3
        return np.floor(((center - self.config.shift) / self.config.tile_size)[0:2]).astype(int)


    def cache(self, object: MetacityObject):
        for lod in range(0, 5):
            model = object.facets.lod[lod]
            for t, n, s in model.items:
                x, y = self.triangle_tile_index(t)
                cache_obj = self.get_object(x, y, object)
                cache_obj.facets.lod[lod].extend(t, n, s)


    def export(self, layer_dir):
        for (x, y), tile in self.tiles.items():
            tile_name = tree.tile_name(x, y)
            cache_path = tree.tile_cache_dir(layer_dir, tile_name)
            obj: MetacityObject
            for obj in tile.values():
                obj.consolidate()
                obj.export(cache_path)



class RegularGridCache:
    def __init__(self, layer_dir):
        self.layer_dir = layer_dir
        self.mem = InMemoryCache(layer_dir)


    def clear_cache(self):
        tree.recreate_cache(self.layer_dir)


    def insert_object(self, object: MetacityObject):
        self.mem.cache(object)
        self.mem.export(self.layer_dir)
        self.mem.clear()



