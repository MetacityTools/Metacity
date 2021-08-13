import os
from typing import Callable, Union

from metacity.geometry.bbox import bboxes_bbox
from metacity.helpers.dirtree import LayerDirectoryTree
from metacity.helpers.file import read_json, write_json
from metacity.io.core import load_model
from metacity.models.model import FacetModel, LineModel, PointModel


class ObjectLODs:
    def __init__(self, level_model: Callable[[], Union[PointModel, LineModel, FacetModel]]):
        self.lod = { lod: level_model() for lod in range(0, 5) }
        self.primitive = level_model


    @property
    def type(self):
        return self.primitive.json_type


    def join_model(self, model: Union[PointModel, LineModel, FacetModel], lod: int):
        self.lod[lod].join_model(model)


    def consolidate(self):
        for lod in range(0, 5):
            if self.lod[lod].exists:
                self.lod[lod].consolidate()


    def load(self, oid: str, base_path: str):
        for lod in range(0, 5):
            self.load_lod(oid, base_path, lod)


    def load_lod(self, oid, base_path, lod):
        input_file = os.path.join(base_path, self.type, str(lod), oid + '.json')
        try:
            self.lod[lod] = load_model(input_file)
        except:
            pass


    def export(self, oid: str, base_path: str):
        for lod in range(0, 5):
            if self.lod[lod].exists:
                self.export_lod(oid, base_path, lod)


    def export_lod(self, oid: str, base_path: str, lod: int):
        data = self.lod[lod].serialize()
        output_file = os.path.join(base_path, self.type, str(lod), oid + '.json')
        write_json(output_file, data)


    def lod_bbox(self, lod):
        return self.lod[lod].bbox


    @property
    def bbox(self):
        return bboxes_bbox([ self.lod_bbox(lod) for lod in range(0, 5) ])




class MetacityObject:
    def __init__(self):
        self.points = ObjectLODs(PointModel)
        self.lines = ObjectLODs(LineModel)
        self.facets = ObjectLODs(FacetModel)
        self.meta = None
        self.oid = None


    def consolidate(self):
        self.points.consolidate()
        self.lines.consolidate()
        self.facets.consolidate()

    
    def load(self, oid: str, base_path: str, dirtree: LayerDirectoryTree):
        self.oid = oid
        self.points.load(oid, base_path)
        self.lines.load(oid, base_path)
        self.facets.load(oid, base_path)
        meta_file = dirtree.metadata_for_oid(self.oid)
        self.meta = read_json(meta_file)


    def export(self, base_path: str, dirtree: LayerDirectoryTree, write_meta=True):
        self.points.export(self.oid, base_path)
        self.lines.export(self.oid, base_path)
        self.facets.export(self.oid, base_path)
        if write_meta:
            meta_file = dirtree.metadata_for_oid(self.oid)
            write_json(meta_file, self.meta)


    def load_base(self, oid: str, dirtree: LayerDirectoryTree):
        base_path = dirtree.geometry_object_dir
        self.load(oid, base_path, dirtree)


    def load_cache(self, oid: str, x: int, y: int, dirtree: LayerDirectoryTree):
        base_path = os.path.join(dirtree.cache_object_dir, dirtree.tile_name(x, y))
        self.load(oid, base_path, dirtree)


    def export_base(self, dirtree: LayerDirectoryTree):
        base_path = dirtree.geometry_object_dir
        self.export(base_path, dirtree)


    def export_cache(self, x: int, y: int, dirtree: LayerDirectoryTree):
        base_path = os.path.join(dirtree.cache_object_dir, dirtree.tile_name(x, y))
        self.export(base_path, dirtree, write_meta=False)


    def lod_bbox(self, lod):
        bboxes_bbox([ self.facets.lod_bbox(lod), self.lines.lod_bbox(lod), self.points.lod_bbox(lod) ])


    @property
    def bbox(self):
        return bboxes_bbox([ self.facets.bbox, self.lines.bbox, self.points.bbox ])


