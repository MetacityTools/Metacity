from metacity.models.model import PointModel, LineModel, FacetModel
from metacity.models.tiles.model import TileModel
from metacity.models.object import ObjectLODs

import numpy as np
from metacity.helpers.dirtree import grid as tree
from metacity.helpers.file import write_json, read_json
from typing import Callable, Union
from metacity.io.core import load_tile
import os


class MetaTileLODs:
    def __init__(self, model_class: Callable[[], Union[PointModel, LineModel, FacetModel]]):
        self.lod = { lod: TileModel(model_class) for lod in range(0, 5) }
        self.primitive_class = model_class


    @property
    def type(self):
        return self.primitive_class.json_type


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
        input_file = tree.path_to_tile_lod(tile_dir, self.type, lod)
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
        output_file = tree.path_to_tile_lod(tile_dir, self.type, lod)
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


    @property
    def name(self):
        return tree.tile_name(self.x, self.y)


    def consolidate(self):
        self.points.consolidate()
        self.lines.consolidate()
        self.facets.consolidate()


    def load(self, x, y, layer_dir):
        tile_name = tree.tile_name(x, y)
        tile_config = tree.tile_config(layer_dir, tile_name)
        tile_dir = tree.tile_dir(tile_name)
        self.points.load(tile_dir)
        self.lines.load(tile_dir)
        self.facets.load(tile_dir)
        self.deserialize(read_json(tile_config))


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


    def export(self, layer_dir):
        tile_dir = tree.tile_dir(layer_dir, self.name)
        tile_config = tree.tile_config(layer_dir, self.name)
        self.points.export(tile_dir)
        self.lines.export(tile_dir)
        self.facets.export(tile_dir)
        write_json(tile_config, self.serialize())


    def join_object(self, object: Union[PointModel, LineModel, FacetModel], bid):
        self.facets.join_models(bid, object.facets)
        self.lines.join_models(bid, object.lines)
        self.points.join_models(bid, object.points)



