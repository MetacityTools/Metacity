from typing import Callable, Union

from metacity.geometry.bbox import bboxes_bbox
from metacity.helpers.dirtree import base as tree
from metacity.helpers.file import read_json, write_json
from metacity.io.core import load_model
from metacity.models.model import FacetModel, LineModel, PointModel


class ObjectLODs:
    def __init__(self, model_class: Callable[[], Union[PointModel, LineModel, FacetModel]]):
        self.lod = { lod: model_class() for lod in range(0, 5) }
        self.primitive_class = model_class


    @property
    def type(self):
        return self.primitive_class.json_type


    def join_model(self, model: Union[PointModel, LineModel, FacetModel], lod: int):
        self.lod[lod].join_model(model)


    def consolidate(self):
        for lod in range(0, 5):
            if self.lod[lod].exists:
                self.lod[lod].consolidate()


    def load(self, oid: str, geometry_path: str):
        for lod in range(0, 5):
            self.load_lod(oid, geometry_path, lod)


    def load_lod(self, oid, geometry_path, lod):
        input_file = tree.path_to_object_lod(geometry_path, self.type, lod, oid)
        try:
            self.lod[lod] = load_model(input_file)
        except:
            pass


    def export(self, oid: str, geometry_path: str):
        for lod in range(0, 5):
            if self.lod[lod].exists:
                self.export_lod(oid, geometry_path, lod)


    def export_lod(self, oid: str, geometry_path: str, lod: int):
        data = self.lod[lod].serialize()
        output_file = tree.path_to_object_lod(geometry_path, self.type, lod, oid)
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

    
    def load(self, oid: str, geometry_path: str, meta_path: str):
        self.oid = oid
        self.points.load(oid, geometry_path)
        self.lines.load(oid, geometry_path)
        self.facets.load(oid, geometry_path)
        meta_file = tree.metadata_for_oid(meta_path, self.oid)
        self.meta = read_json(meta_file)


    def export(self, geometry_path: str, meta_path=""):
        self.points.export(self.oid, geometry_path)
        self.lines.export(self.oid, geometry_path)
        self.facets.export(self.oid, geometry_path)
        if len(meta_path) > 0:
            meta_file = tree.metadata_for_oid(meta_path, self.oid)
            write_json(meta_file, self.meta)


    def lod_bbox(self, lod):
        bboxes_bbox([ self.facets.lod_bbox(lod), self.lines.lod_bbox(lod), self.points.lod_bbox(lod) ])


    @property
    def bbox(self):
        return bboxes_bbox([ self.facets.bbox, self.lines.bbox, self.points.bbox ])


