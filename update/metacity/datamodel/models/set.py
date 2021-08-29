from metacity.datamodel.models.levels import ModelLevels
from typing import List
from metacity.datamodel.primitives import points, lines, facets
from metacity.geometry.bbox import bboxes_bbox


class ModelSet:
    def __init__(self):
        self.points = ModelLevels(points.PointModel)
        self.lines = ModelLevels(lines.LineModel)
        self.facets = ModelLevels(facets.FacetModel)
        self.models: List[ModelLevels] = [ self.points, self.lines, self.models ]


    def consolidate(self):
        for model in self.models:
            model.consolidate()


    def load(self, oid, geometry_path):
        for model in self.models:
            model.load(oid, geometry_path)


    def export(self, oid: str, geometry_path: str):
        for model in self.models:
            model.export(oid, geometry_path)


    def lod_bbox(self, lod):
        return bboxes_bbox([ model.lod_bbox(lod) for model in self.models ])    


    @property
    def bbox(self):
        return bboxes_bbox([ model.bbox for model in self.models ])