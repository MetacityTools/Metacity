import json
import os
from typing import Callable, Union

from metacity.helpers.dirtree import DirectoryTreePaths
from metacity.helpers.file import write_json
from metacity.io.cj import load_cityjson_object
from metacity.models.model import FacetModel, NonFacetModel


class ObjectLODs:
    def __init__(self, level_model: Callable[[], Union[NonFacetModel,FacetModel]]):
        self.lod = { lod: level_model() for lod in range(0, 6) }


    def join_model(self, model, lod):
        self.lod[lod].join_model(model)


    def consolidate(self):
        for lod in range(0, 6):
            if self.lod[lod].exists():
                self.lod[lod].consolidate()


    def export(self, paths, oid):
        for lod in range(0, 6):
            if self.lod[lod].exists():
                self.export_lod(paths, lod, oid)


    def export_lod(self, paths, lod, oid):
        data = self.lod[lod].serialize()
        output_dir = self.lod_directory(paths, lod)
        output_file = os.path.join(output_dir, oid + '.json')
        write_json(output_file, data)



class PointObjectLODs(ObjectLODs):
    def __init__(self):
        super().__init__(NonFacetModel)


    def lod_directory(self, paths, lod):
        return paths.use_directory(os.path.join(paths.point_geometry, lod))



class LineObjectLODs(ObjectLODs):
    def __init__(self):
        super().__init__(NonFacetModel)


    def lod_directory(self, paths, lod):
        return paths.use_directory(os.path.join(paths.line_geometry, lod))



class FacetObjectLODs(ObjectLODs):
    def __init__(self):
        super().__init__(FacetModel)


    def lod_directory(self, paths, lod):
        return paths.use_directory(os.path.join(paths.facet_geometry, str(lod)))



class MetacityObject:
    def __init__(self):
        self.points = PointObjectLODs()
        self.lines = LineObjectLODs()
        self.facets = FacetObjectLODs()
        self.meta = None


    def load_cityjson_object(self, oid, object, vertices):
        self.oid = oid
        load_cityjson_object(self, object, vertices)


    def consolidate(self):
        self.points.consolidate()
        self.lines.consolidate()
        self.facets.consolidate()

    def export(self, paths: DirectoryTreePaths):
        self.points.export(paths, self.oid)
        self.lines.export(paths, self.oid)
        self.facets.export(paths, self.oid)
        meta_file = os.path.join(paths.metadata, self.oid + '.json')
        write_json(meta_file, self.meta)




