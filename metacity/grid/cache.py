from typing import Dict
import numpy as np
from metacity.grid.config import RegularGridConfig
from metacity.models.object import MetacityObject, ObjectLODs
from metacity.helpers.dirtree import LayerDirectoryTree


class RegularGridCache:
    def __init__(self, config: RegularGridConfig, dirtree: LayerDirectoryTree):
        self.config = config
        self.dirtree = dirtree
        self.tiles = {}


    def clear_cache(self):
        self.dirtree.recreate_cache()


    def triangle_tile_index(self, triangle):
        center = np.sum(triangle, axis=0) / 3
        return np.floor(((center - self.config.shift) / self.config.tile_size)[0:2]).astype(int)


    def copy_lod_semantics(self, original: ObjectLODs, copy: ObjectLODs):
        for lod in range(0, 5):
            copy.lod[lod].semantics_meta = original.lod[lod].semantics_meta
            

    def copy_semantics(self, object, cache_obj):
        self.copy_lod_semantics(object.facets, cache_obj.facets)
        self.copy_lod_semantics(object.lines, cache_obj.lines)
        self.copy_lod_semantics(object.points, cache_obj.points)


    def create_cache_obj(self, object: MetacityObject, tile: Dict[str, MetacityObject]):
        cache_obj = MetacityObject()
        cache_obj.oid = object.oid
        cache_obj.meta = object.meta
        self.copy_semantics(object, cache_obj)
        tile[object.oid] = cache_obj
        return cache_obj


    def get_cache_object(self, x, y, object: MetacityObject):
        if (x, y) not in self.tiles:
            self.tiles[(x, y)] = {}
        tile = self.tiles[(x, y)]
        if object.oid not in tile:
            return self.create_cache_obj(object, tile)
        return tile[object.oid]


    def cache_facets(self, object: MetacityObject):
        for lod in range(0, 5):
            model = object.facets.lod[lod]
            for t, n, s in model.items:
                x, y = self.triangle_tile_index(t)
                cache_obj = self.get_cache_object(x, y, object)
                cache_obj.facets.lod[lod].extend(t, n, s)
                

    def cache_object(self, object: MetacityObject):
        self.tiles = {}
        self.cache_facets(object)
        self.cache_processed_tiles()
        self.tiles = {}


    def cache_processed_tiles(self):
        for (x, y), tile in self.tiles.items():
            for obj in tile.values():
                obj.consolidate()
                obj.export_cache(x, y, self.dirtree) 


    


