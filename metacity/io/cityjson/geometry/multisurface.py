from metacity.io.cityjson.geometry.base import CJBasePrimitive, rep_nones, gen_nones
import numpy as np
import itertools
from earcut import earcut as ec


def generate_hole_indices(surface):
    #manage holes for triangulation
    if len(surface) <= 1:
        return None
    face_lengths = [ len(h) for h in surface ]
    face_length_sums = [ i for i in itertools.accumulate(face_lengths) ]
    return face_length_sums[:-1]


def parse_surface_vertices(surface, vertices):
    hole_indices = generate_hole_indices(surface)  

    vi = np.array([ val for sublist in surface for val in sublist ]) #flatten irregularly-shaped list of lists
    vs = vertices[vi]
    
    normal, normal_exists = ec.normal(vs.flatten())

    if not normal_exists: 
        #The model contains face which couldn't be triangulated.
        return None, None, None

    ti = ec.earcut(vs.flatten(), hole_indices, 3)

    v = np.array(vs[ti], dtype=np.float32)
    tri_count = len(ti) 
    n = np.repeat([normal], tri_count, axis=0).astype(np.float32)    
    return v, n, tri_count


class CJSurface:
    def __init__(self, vertices=None, normals=None, semantics=None):
        self.v = [] if vertices is None else vertices
        self.n = [] if normals is None else normals
        self.s = [] if semantics is None else semantics


    def join(self, surface):
        self.v.extend(surface.v)
        self.n.extend(surface.n)
        self.s.extend(surface.s)


def parse_vertices(boundaries, vertices):
    v, n, lengths = [], [], []
    for surface in boundaries:
        sv, sn, l = parse_surface_vertices(surface, vertices)
        #maybe not the best solution
        if sv is None:
            lengths.append(0)
            continue
        v.extend(sv)
        n.extend(sn)
        lengths.append(l)


    v = np.array(v, dtype=np.float32).flatten()
    n = np.array(n, dtype=np.float32).flatten()
    return v, n, lengths


def parse_semantics(semantic_values, surface_lengths):
    if semantic_values != None:
        buffer = np.repeat(rep_nones(semantic_values), surface_lengths)
    else:
        buffer = gen_nones(sum(surface_lengths))

    return np.array(buffer, dtype=np.int32)


class CJMultiSurface(CJBasePrimitive):
    def __init__(self, data, vertices):
        super().__init__(data)
        boundaries = data["boundaries"]
        semantics = self.preprocess_semantics(data)
        surface = self.parse(boundaries, semantics, vertices)
        self.extract_surface(surface)


    def parse(self, boundaries, semantics, vertices):
        v, n, l = parse_vertices(boundaries, vertices)
        if semantics != None:
            semantics = parse_semantics(semantics, l)
        else:
            semantics = gen_nones(sum(l))

        semantics = np.array(semantics, dtype=np.int32)
        return CJSurface(v, n, semantics)


    def extract_surface(self, surface):
        self.vertices = np.array(surface.v, dtype=np.float32) 
        self.normals = np.array(surface.n, dtype=np.float32)
        self.semantics = np.array(surface.s, dtype=np.int32)


    def preprocess_semantics(self, data):
        if "semantics" in data:
            semantics = data["semantics"]["values"]
            self.meta = data["semantics"]["surfaces"]
        else:
            semantics = None
            self.meta = []
        return semantics

