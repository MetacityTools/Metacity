import json

import numpy as np
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.filesystem import layer as fs
from metacity.io.cityjson.object import CJObject
from tqdm import tqdm


class CJParser:
    def __init__(self, input_file: str):
        with open(input_file, "r") as file:
            contents = json.load(file)

        self.objects = contents["CityObjects"]
        if "geometry-templates" in contents:
            self.templates = contents["geometry-templates"]
        else:
            self.templates = None
        self.vertices = np.array(contents["vertices"])

    @property
    def is_empty(self):
        return len(self.vertices) == 0 or len(self.objects) == 0

    def adjust_data(self, layer: MetacityLayer):
        layer.config.apply(self.vertices)

    def parse_and_export(self, layer: MetacityLayer):
        for oid, data in tqdm(self.objects.items()):
            object = CJObject(oid, data, self.vertices, self.templates)
            object.export(layer.geometry_path, layer.meta_path)


def parse(layer: MetacityLayer, input_file: str):
    fs.copy_to_layer(layer.dir, input_file)
    parser = CJParser(input_file)
    parser.adjust_data(layer)
    parser.parse_and_export(layer)
