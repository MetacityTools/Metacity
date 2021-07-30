import os
from metacity.helpers.dirtree import LayerDirectoryTree
from typing import Callable, Union

from metacity.helpers.file import read_json, write_json
from metacity.io.core import load_model
from metacity.models.model import FacetModel, NonFacetModel


class ObjectLODs:
    def __init__(self, level_model: Callable[[], Union[NonFacetModel,FacetModel]]):
        self.lod = { lod: level_model() for lod in range(0, 5) }


    def join_model(self, model: Union[FacetModel, NonFacetModel], lod: int):
        self.lod[lod].join_model(model)


    def consolidate(self):
        for lod in range(0, 5):
            if self.lod[lod].exists():
                self.lod[lod].consolidate()


    def load(self, oid: str, dirtree: LayerDirectoryTree):
        for lod in range(0, 5):
            input_dir = self.lod_directory(dirtree, lod)
            input_file = os.path.join(input_dir, oid + '.json')
            try:
                self.lod[lod] = load_model(input_file)
            except:
                continue


    def export(self, oid: str, dirtree: LayerDirectoryTree):
        for lod in range(0, 5):
            if self.lod[lod].exists():
                self.export_lod(oid, dirtree, lod)


    def export_lod(self, oid: str, dirtree: LayerDirectoryTree, lod: int):
        data = self.lod[lod].serialize()
        output_dir = self.lod_directory(dirtree, lod)
        output_file = os.path.join(output_dir, oid + '.json')
        write_json(output_file, data)



class PointObjectLODs(ObjectLODs):
    def __init__(self):
        super().__init__(NonFacetModel)


    def lod_directory(self, dirtree: LayerDirectoryTree, lod: int):
        return dirtree.point_geometry_lod_dir(lod)



class LineObjectLODs(ObjectLODs):
    def __init__(self):
        super().__init__(NonFacetModel)


    def lod_directory(self, dirtree: LayerDirectoryTree, lod: int):
        return dirtree.line_geometry_lod_dir(lod)



class FacetObjectLODs(ObjectLODs):
    def __init__(self):
        super().__init__(FacetModel)


    def lod_directory(self, dirtree: LayerDirectoryTree, lod: int):
        return dirtree.facet_geometry_lod_dir(lod)



class MetacityObject:
    def __init__(self):
        self.points = PointObjectLODs()
        self.lines = LineObjectLODs()
        self.facets = FacetObjectLODs()
        self.meta = None
        self.oid = None


    def consolidate(self):
        self.points.consolidate()
        self.lines.consolidate()
        self.facets.consolidate()


    def load(self, oid: str, dirtree: LayerDirectoryTree):
        self.oid = oid
        self.points.load(oid, dirtree)
        self.lines.load(oid, dirtree)
        self.facets.load(oid, dirtree)
        meta_file = dirtree.metadata_for_oid(self.oid)
        self.meta = read_json(meta_file)


    def export(self, dirtree: LayerDirectoryTree):
        self.points.export(self.oid, dirtree)
        self.lines.export(self.oid, dirtree)
        self.facets.export(self.oid, dirtree)
        meta_file = dirtree.metadata_for_oid(self.oid)
        write_json(meta_file, self.meta)




