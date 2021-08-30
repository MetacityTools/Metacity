import json
from typing import Dict, List

import numpy as np
from metacity.datamodel.layer.layer import MetacityLayer
import itertools
from metacity.filesystem import layer as fs
from tqdm import tqdm
from earcut import earcut as ec


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
    

def generate_hole_indices(surface):
    #manage holes for triangulation
    if len(surface) <= 1:
        return None
    face_lengths = [ len(h) for h in surface ]
    face_length_sums = [ i for i in itertools.accumulate(face_lengths) ]
    return face_length_sums[:-1]


def parse_surface(surface, vertices):
    hole_indices = generate_hole_indices(surface)  

    vi = np.array([ val for sublist in surface for val in sublist ]) #flatten irregularly-shaped list of lists
    vs = vertices[vi]
    normal, normal_exists = ec.normal(vs.flatten())

    if not normal_exists:  
        raise Exception("The model contains face which couldn't be triangulated.")
    
    ti = ec.earcut(vs.flatten(), hole_indices, 3)

    v = np.array(vs[ti], dtype=np.float32)
    tri_count = len(ti) 
    n = np.repeat([normal], tri_count, axis=0).astype(np.float32)    
    return v, n, tri_count


class CJSurface:
    def __init__(self, vertices=[], normals=[], semantics=[]):
        self.v = vertices
        self.n = normals
        self.s = semantics


    def join(self, surface):
        self.v.extend(surface.v)
        self.n.extend(surface.n)
        self.s.extend(surface.s)


def parse_vertices(boundaries, vertices):
    v, n, lengths = [], [], []
    for surface in boundaries:
        try:
            sv, sn, l = parse_surface(surface, vertices)
            v.extend(sv)
            n.extend(sn)
            lengths.append(l)
        except:
            pass

    v = np.array(v, dtype=np.float32).flatten()
    n = np.array(n, dtype=np.float32).flatten()
    return v, n, lengths


def parse_semantics(semantic_values, surface_lengths):
    if semantic_values != None:
        assert len(semantic_values) == len(surface_lengths)
        values = [ rep_nones(v) for v in semantic_values ]
        buffer = np.repeat(values, surface_lengths)
    else:
        buffer = gen_nones(sum(surface_lengths))

    return np.array(buffer, dtype=np.int32)


def parse_surface(boundaries, semantics, vertices):
    v, n, l = parse_vertices(boundaries, vertices)
    if semantics != None:
        semantic_values = semantics["values"]
        semantics = parse_semantics(semantic_values, l)
    else:
        semantics = gen_nones(sum(l))

    return CJSurface(v, n, semantics)


class CJMultiSurface(CJBasePrimitive):
    def __init__(self, data, vertices):
        super().__init__()
        boundaries = data["boundaries"]
        semantics = self.preprocess_semantics(data)

        surface = parse_surface(boundaries, semantics, vertices)
        self.extract_surface(surface)


    def extract_surface(self, surface):
        self.vertices = surface.v 
        self.normals = surface.n
        self.semantics = surface.s


    def preprocess_semantics(self, data):
        if "semantics" in data:
            semantics = data["semantics"]
            self.meta = semantics["surfaces"]
        else:
            semantics = None
            self.meta = []
        return semantics


def ensure_iterable(data):
    try:
        _ = iter(data)
        return data
    except TypeError:
        return [ data ]


def parse_solid(boundaries, semantics, vertices):
    surface = CJSurface()
    for shell, shell_semantics in itertools.zip_longest(boundaries, ensure_iterable(semantics)):
        s = parse_surface(shell, shell_semantics, vertices)
        surface.join(s)

    return surface
    

class CJSolid(CJMultiSurface):
    def __init__(self, data, vertices):
        super().__init__()
        boundaries = data["boundaries"]
        semantics = self.preprocess_semantics(data)
        surface = parse_solid(boundaries, semantics, vertices)
        self.extract_surface(surface)


def parse_multisolid(boundaries, semantics, vertices):
    surface = CJSurface()
    for solid, solid_semantic in itertools.zip_longest(boundaries, ensure_iterable(semantics)):
        s = parse_solid(solid, solid_semantic, vertices)
        surface.join(s)

    return surface


class CJMultiSolid(CJMultiSurface):
    def __init__(self, data, vertices):
        super().__init__()
        boundaries = data["boundaries"]
        semantics = self.preprocess_semantics(data)
        surface = parse_multisolid(boundaries, semantics, vertices)
        self.extract_surface(surface)


class CJGeometryInstance:
    def __init__(self, data, templates):
        #TODO
        pass


class CJGeometry:
    def __init__(self, data, vertices, templates):
        self.type = data["type"].lower()

        #if self.type == 'geometryinstance':
        #    #because geometry instance does not have specified LOD
        #    self.primitive = CJGeometryInstance(data, templates)

        self.lod = data["lod"]

        if self.type == 'multipoint':
            self.primitive = CJPoints(data, vertices)
        elif self.type == 'multilinestring':
            self.primitive = CJLines(data, vertices)
        elif self.type == 'multisurface' or self.type == 'compositesurface':
            self.primitive = CJMultiSurface(data, vertices)
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

    


