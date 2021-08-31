from typing import List

from numpy.lib.function_base import append

from metacity.datamodel.primitives.base import BaseModel
from metacity.utils.bbox import bboxes_bbox
from metacity.filesystem import base as fs
from metacity.filesystem.file import read_json, write_json


class ModelSet:
    def __init__(self):
        self.models: List[BaseModel] = []

    #TODO tba
    def export(self, oid: str, geometry_path: str):
        for i, model in enumerate(self.models):
            data = model.serialize()
            output_dir = fs.path_to_object(geometry_path, oid)
            fs.create_dir_if_not_exists(output_dir)
            output_file = fs.path_to_model(output_dir, 'model' + str(i) + '.json')
            write_json(output_file, data)


    def load(self, oid, geometry_path):
        for model in fs.object_models(geometry_path, oid):
            read_json(model)
            self.models.append()


    @property
    def bbox(self):
        return bboxes_bbox([ model.bbox for model in self.models ])
