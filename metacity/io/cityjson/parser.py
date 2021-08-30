import json
from typing import Dict, List

import numpy as np
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.filesystem import layer as fs
from tqdm import tqdm


def rep_nones(data):
        return [ i if i != None else -1 for i in data]


def gen_nones(elements_count):
    return [ -1 ] * elements_count


class CJBasePrimitive:
    def __init__(self):
        pass

    def generate_semantics(self, elements_count):
        self.semantics = np.array(gen_nones(elements_count), dtype=np.int32)
        self.meta = []


class CJPoints(CJBasePrimitive):
    def __init__(self, data, vertices):
        super().__init__()
        self.vertices = self.parse_vertices(data, vertices)
        elements_count = len(self.vertices) // 3

        if "semantics" in data:
            self.parse_semantics(data["semantics"], elements_count)
        else:
            self.generate_semantics(elements_count)


    def parse_vertices(self, data, vertices):
        return np.array(vertices[data["boundaries"]], dtype=np.float32).flatten()


    def parse_semantics(self, semantics, elements_count):
        if semantics["values"] != None:
            buffer = rep_nones(semantics["values"])
        else:
            buffer = gen_nones(elements_count)

        self.semantics = np.array(buffer, dtype=np.int32)
        self.meta = semantics["surfaces"]



class CJLines(CJBasePrimitive):
    def __init__(self, data, vertices):
        super().__init__()
        self.vertices, segment_lengths = self.parse_vertices(data, vertices)
        elements_count = len(self.vertices) // 3
        
        if "semantics" in data:
            self.parse_semantics(data["semantics"], segment_lengths)
        else:
            self.generate_semantics(elements_count)


    def parse_vertices(self, data, vertices):
        v, segment_lengths = [], []
        for segment in data["boundaries"]:
            length = 0
            for start, end in zip(segment, segment[1:]):
                v.extend((vertices[start], vertices[end]))
                length += 2
            segment_lengths.append(length)
        return np.array(v, dtype=np.float32).flatten(), segment_lengths


    def parse_semantics(self, semantics, segment_lengths):
        if semantics["values"] != None:
            buffer = rep_nones(semantics["values"]) 
            buffer = np.repeat(buffer, segment_lengths)
        else:
            buffer = gen_nones(sum(segment_lengths))

        self.semantics = np.array(buffer, dtype=np.int32)
        self.meta = semantics["surfaces"]
    



class CJMultisurface:
    def __init__(self, data, vertices):
        pass


class CJSolid:
    def __init__(self, data, vertices):
        pass


class CJMultiSolid:
    def __init__(self, data, vertices):
        pass


class CJGeometryInstance:
    def __init__(self, data, templates):
        #TODO
        pass


class CJGeometry:
    def __init__(self, data, vertices, templates):
        self.type = data["type"].lower()

        if self.type == 'geometryinstance':
            #because geometry instance does not have specified LOD
            self.primitive = CJGeometryInstance(data, templates)
        else:
            self.lod = data["lod"]

            if self.type == 'multipoint':
                self.primitive = CJPoints(data, vertices)
            elif self.type == 'multilinestring':
                self.primitive = CJLines(data, vertices)
            elif self.type == 'multisurface' or self.type == 'compositesurface':
                self.primitive = CJMultisurface(data, vertices)
            elif self.type == 'solid':
                self.primitive = CJSolid(data, vertices)
            elif self.type == 'multisolid' or self.type == 'compositesolid':
                self.primitive = CJMultiSolid(data, vertices)



class CJObject:
    def __init__(self, oid: str, data: Dict, vertices, templates):
        self.oid = oid
        self.meta = self.clean_meta(data)
        self.geometry: List[CJGeometry] = self.parse_geometry(data, vertices, templates)


    def clean_meta(self, data):
        return { key: value for key, value in data.items() if key not in ['geometry', 'semantics'] }


    def parse_geometry(self, data, vertices, templates):
        geometry = data['geometry']
        geometries = []
        for geometry_object in geometry:
            geometries.append(CJGeometry(geometry_object, vertices, templates))
        return geometries



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

    


