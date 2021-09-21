from typing import Callable, Dict, List

from metacity.datamodel.primitives.base import BaseModel
from metacity.datamodel.primitives.facets import FacetModel
from metacity.datamodel.primitives.lines import LineModel
from metacity.datamodel.primitives.points import PointModel
from metacity.filesystem import base as fs
from metacity.filesystem.file import read_json, write_json
from metacity.utils.bbox import bboxes_bbox, empty_bbox


PRIMITIVES: Dict[str, Callable[[], BaseModel]] = {
    PointModel.TYPE: PointModel,
    LineModel.TYPE: LineModel,
    FacetModel.TYPE: FacetModel
}


class ModelSet:
    def __init__(self):
        self.models: List[BaseModel] = []

    def export(self, oid: str, geometry_path: str):
        output_dir = fs.path_to_object(geometry_path, oid)
        fs.create_dir_if_not_exists(output_dir)

        for i, model in enumerate(self.models):
            data = model.serialize()
            name = f'model_{i}_{model.TYPE}.json'
            output_file = fs.path_to_model(output_dir, name)
            write_json(output_file, data)

    def load(self, oid, geometry_path):
        for model in fs.object_models(geometry_path, oid):
            data = read_json(model)
            if not self.validate(model, data):
                continue
            primitive = PRIMITIVES[data['type']]()
            primitive.deserialize(data)
            self.models.append(primitive)

    def delete(self, oid, geometry_path):
        output_dir = fs.path_to_object(geometry_path, oid)
        self.models = []
        fs.remove_dirtree(output_dir)

    def split(self, x_planes, y_planes):
        splitted = ModelSet()
        for model in self.models:
            splitted.models.extend(model.split(x_planes, y_planes))
        return splitted

    def validate(self, model, data):
        if fs.filename(model) == 'config.json':
            return False
        if 'type' not in data:
            print(f'Model missing model type: {model}')
            return False
        if data['type'] not in PRIMITIVES:
            print(f'Unknown model type: {data["type"]} in {model}')
            return False
        return True

    @property
    def bbox(self):
        if len(self.models) == 0:
            return empty_bbox()
        return bboxes_bbox([model.bbox for model in self.models])


