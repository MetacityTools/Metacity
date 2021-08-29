from typing import Callable

from metacity.datamodel.primitives.base import BaseModel
from metacity.filesystem import base as fs
from metacity.filesystem.file import read_json, write_json
from metacity.geometry.bbox import bboxes_bbox


class ModelLevels:
    def __init__(self, model_class: Callable[[], BaseModel]):
        self.lod = { lod: model_class() for lod in range(0, 5) }
        self.primitive_class = model_class


    @property
    def type(self):
        return self.primitive_class.TYPE


    @property
    def bbox(self):
        return bboxes_bbox([ self.lod_bbox(lod) for lod in range(0, 5) ])


    def lod_bbox(self, lod):
        return self.lod[lod].bbox


    def load(self, oid: str, geometry_path: str):
        for lod in range(0, 5):
            self.load_lod(oid, geometry_path, lod)


    def load_lod(self, oid, geometry_path, lod):
        input_file = fs.path_to_object_lod(geometry_path, self.type, lod, oid)
        
        if not fs.file_exists(input_file):
            return

        self.load_model(input_file, lod)


    def load_model(self, input_file, lod):
        model_data = read_json(input_file)
        model = self.primitive_class()
        model.deserialize(model_data)
        self.lod[lod] = model


    def export(self, oid: str, geometry_path: str):
        for lod in range(0, 5):
            if self.lod[lod].exists:
                self.export_lod(oid, geometry_path, lod)


    def export_lod(self, oid: str, geometry_path: str, lod: int):
        data = self.lod[lod].serialize()
        output_file = fs.path_to_object_lod(geometry_path, self.type, lod, oid)
        write_json(output_file, data)




