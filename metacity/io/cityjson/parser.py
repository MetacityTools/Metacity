import json
from typing import List

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
        self.templates = contents["geometry-templates"] if "geometry-templates" in contents else None
        self.vertices = np.array(contents["vertices"])
        self.parsed_objects: List[CJObject] = []


    @property
    def is_empty(self):
        return len(self.vertices) == 0 or len(self.objects) == 0


#    def apply_config(self, layer: MetacityLayer):
#        config = layer.config
#        if layer.empty:
#            config.update(self.vertices)
#        config.apply(self.vertices)
#        config.export(layer.dir)
#
    
    def parse(self):
        for oid, data in tqdm(self.objects.items()):
            self.parsed_objects.append(CJObject(oid, data, self.vertices, self.templates))




def parse(layer: MetacityLayer, input_file: str):
    fs.copy_to_layer(layer.dir, input_file)
    parser = CJParser(input_file)
    parser.parse()

    


