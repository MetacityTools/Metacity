from metacity.grid.config import RegularGridConfig
from metacity.models.model import PointModel, LineModel, FacetModel
from metacity.models.tiles.model import TileModel
from metacity.models.object import MetacityObject, ObjectLODs

import numpy as np
from metacity.helpers.dirtree import LayerDirectoryTree
from metacity.helpers.file import write_json, read_json
from typing import Callable, Union
from metacity.io.core import load_tile
import os


class MetaTileLODs:
    def __init__(self, level_model: Callable[[], Union[PointModel, LineModel, FacetModel]]):
        self.lod = { lod: TileModel(level_model) for lod in range(0, 5) }
        self.primitive = level_model


    @property
    def type(self):
        return self.primitive.json_type


    def join_models(self, bid: int, modelLODs: ObjectLODs):
        for lod in range(0, 5):
            if modelLODs.lod[lod].exists:
                self.lod[lod].join_primitive_model(bid, modelLODs.lod[lod])


    def consolidate(self):
        for lod in range(0, 5):
            if self.lod[lod].exists:
                self.lod[lod].consolidate()
            

    def load(self, tile_dir: str):
        for lod in range(0, 5):
            self.load_lod(tile_dir, lod)


    def load_lod(self, tile_dir: str, lod: int):
        input_file = os.path.join(tile_dir, str(lod), self.type + '.json')
        try:
            self.lod[lod] = load_tile(input_file)
        except:
            pass


    def export(self, tile_dir: str):
        for lod in range(0, 5):
            if self.lod[lod].exists:
                self.export_lod(tile_dir, lod)


    def export_lod(self, tile_dir: str, lod: int):
        data = self.lod[lod].serialize()
        output_file = os.path.join(tile_dir, str(lod), self.type + '.json')
        write_json(output_file, data)



class MetaTile:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.bbox = np.array([0, 0, 0])
        self.objects = 0

        self.facets = MetaTileLODs(FacetModel)
        self.lines = MetaTileLODs(LineModel)
        self.points = MetaTileLODs(PointModel)


    def consolidate(self):
        self.points.consolidate()
        self.lines.consolidate()
        self.facets.consolidate()


    def load(self, x, y, dirtree: LayerDirectoryTree):
        tile_dir = dirtree.tile_dir(x, y)
        self.points.load(tile_dir)
        self.lines.load(tile_dir)
        self.facets.load(tile_dir)
        self.deserialize(read_json(dirtree.tile_config(x, y)))


    def serialize(self):
            return {
                'x': self.x,
                'y': self.y,
                'bbox': self.bbox.tolist(),
                'objects': self.objects
            }


    def deserialize(self, data):
        self.x = data['x']
        self.y = data['y']
        self.bbox = np.array(data['bbox'])
        self.objects = data['objects']


    def export(self, dirtree: LayerDirectoryTree):
        tile_dir = dirtree.tile_dir(self.x, self.y)
        self.points.export(tile_dir)
        self.lines.export(tile_dir)
        self.facets.export(tile_dir)
        write_json(dirtree.tile_config(self.x, self.y), self.serialize())


    def join_object(self, object, bid):
        self.facets.join_models(bid, object.facets)
        self.lines.join_models(bid, object.lines)
        self.points.join_models(bid, object.points)


    def build_from_cache(self, dirtree: LayerDirectoryTree, config: RegularGridConfig):
        for oid in dirtree.objects_in_tile_cache(self.x, self.y):
            object = MetacityObject()
            object.load_cache(oid, self.x, self.y, dirtree)
            bid = config.id_for_oid(object.oid)
            self.join_object(object, bid)
            self.objects += 1

        self.consolidate()
        self.export(dirtree)



