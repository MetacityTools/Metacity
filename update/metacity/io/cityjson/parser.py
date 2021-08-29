import json
from typing import Dict
from update.metacity.datamodel.object import MetacityObject

import numpy as np
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.io.cityjson.objects import parse_object
from metacity.filesystem import layer as fs
from tqdm import tqdm


class CJParser:
    def __init__(self, input_file: str):
        with open(input_file, "r") as file:
            contents = json.load(file)

        self.objects = contents["CityObjects"] 
        self.vertices = np.array(contents["vertices"])


    @property
    def is_empty(self):
        return len(self.vertices) == 0 or len(self.objects) == 0


    def apply_config(self, layer: MetacityLayer):
        config = layer.config
        if layer.empty:
            config.update(self.vertices)
        config.apply(self.vertices)
        config.export(layer.dir)


    def parse_objects(self, layer: MetacityLayer):
        geometry_path = layer.geometry_path
        meta_path = layer.meta_path

        for oid, cjobject in tqdm(self.objects.items()):
            obj = MetacityObject()
            parse_object(obj, self.vertices, cjobject)
            obj.oid = oid
            obj.export(geometry_path, meta_path)



def parse(layer: MetacityLayer, input_file: str):
    fs.copy_to_layer(layer.dir, input_file)
    parser = CJParser(layer, input_file)
    if not parser.is_empty:
        parser.apply_config(layer)
        parser.parse_objects(layer)
    