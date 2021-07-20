from models.points import PointModel
from models.lines import LineModel
from models.facets import MultifacetedModel
from helpers.dirtree import DirectoryTreePaths
from helpers.file import id_from_filename

import ntpath
import json
import os



class MetacityModel:
    def __init__(self):
        self.points = PointModel()
        self.lines = LineModel()
        self.facets = MultifacetedModel()
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


    def export(self, paths: DirectoryTreePaths):
        self.points.export(paths, self.oid)
        self.lines.export(paths, self.oid)
        self.facets.export(paths, self.oid)