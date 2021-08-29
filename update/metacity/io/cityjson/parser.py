import json
from typing import Dict
from update.metacity.datamodel.object import MetacityObject

import numpy as np
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.io.cityjson.objects import CJObjectParser
from metacity.filesystem import layer as fs
from tqdm import tqdm


class CityJSONParser:
    def __init__(self, layer: MetacityLayer, input_file: str):
        self.layer = layer
        self.input_file = input_file


    def load(self):
        fs.copy_to_layer(self.layer.dir, self.input_file)
        parse_input_file(self)
        if is_empty(self):
            return
        apply_config(self)
        process_objects(self)


def is_empty(loader: CityJSONParser):
    return len(loader.vertices) == 0 or len(loader.objects) == 0


def parse_input_file(loader: CityJSONParser):
    with open(loader.input_file, "r") as file:
        contents = json.load(file)
    loader.objects = contents["CityObjects"] 
    loader.vertices = np.array(contents["vertices"])


def apply_config(loader: CityJSONParser):
    config = loader.layer.config
    if loader.layer.empty:
        config.update(loader.vertices)
    config.apply(loader.vertices)
    config.export(loader.layer.dir)


def process_objects(loader: CityJSONParser):
    geometry_path = loader.layer.geometry_path
    meta_path = loader.layer.meta_path

    for oid, object in tqdm(loader.objects.items()):
        obj = MetacityObject()
        parser = CJObjectParser(loader.vertices, oid, object)
        parser.parse(obj)
        obj.export(geometry_path, meta_path)

