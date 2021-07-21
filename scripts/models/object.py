import json
import os
from typing import Callable, Union

from helpers.dirtree import DirectoryTreePaths
from helpers.file import id_from_filename

from models.model import FacetModel, NonFacetModel


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
        self.write(output_file, data)


    def write(self, filename, data):
        if os.path.exists(filename):
            print(f'File {filename} already exixsts, rewriting...')
            os.remove(filename)

        with open(filename, 'w') as file:
            json.dump(data, file)



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
        self.json = None


    def load_cityjson_object(self, object_file_path):
        with open(object_file_path, "r") as file:
            self.json = json.load(file)
            self.oid = id_from_filename(object_file_path)


    @property
    def geometry(self):
        if self.json == None:
            raise Exception("No input CityJSON Object loaded.")
        return self.json["geometry"]


    def consolidate(self):
        self.points.consolidate()
        self.lines.consolidate()
        self.facets.consolidate()


    def export(self, paths: DirectoryTreePaths):
        self.points.export(paths, self.oid)
        self.lines.export(paths, self.oid)
        self.facets.export(paths, self.oid)
