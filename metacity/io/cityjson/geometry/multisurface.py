import itertools
from metacity.utils.surface import Surface

import numpy as np
from earcut import earcut as ec
from metacity.datamodel.primitives.facets import FacetModel
from metacity.io.cityjson.geometry.base import (CJBasePrimitive, gen_nones,
                                                rep_nones)


def generate_hole_indices(surface):
    # manage holes for triangulation
    if len(surface) <= 1:
        return None
    face_lengths = [len(h) for h in surface]
    face_length_sums = [i for i in itertools.accumulate(face_lengths)]
    return face_length_sums[:-1]


def parse_surface_vertices(surface, vertices):
    hole_indices = generate_hole_indices(surface)
    # flatten irregularly-shaped list of lists
    vi = np.array([val for sublist in surface for val in sublist])
    vs = vertices[vi]
    normal, normal_exists = ec.normal(vs.flatten())

    if not normal_exists:
        # The model contains face which couldn't be triangulated.
        return None, None, None

    ti = ec.earcut(vs.flatten(), hole_indices, 3)
    v = np.array(vs[ti], dtype=np.float32)
    tri_count = len(ti)
    n = np.repeat([normal], tri_count, axis=0).astype(np.float32)
    return v, n, tri_count


def parse_vertices(boundaries, vertices):
    v, n, lengths = [], [], []
    for surface in boundaries:
        sv, sn, ln = parse_surface_vertices(surface, vertices)
        # maybe not the best solution
        if sv is None:
            lengths.append(0)
            continue
        v.extend(sv)
        n.extend(sn)
        lengths.append(ln)

    vs = np.array(v, dtype=np.float32).flatten()
    ns = np.array(n, dtype=np.float32).flatten()
    return vs, ns, lengths


def parse_semantics(semantic_values, surface_lengths):
    if semantic_values is not None:
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
        v, n, ln = parse_vertices(boundaries, vertices)
        if semantics is not None:
            semantics = parse_semantics(semantics, ln)
        else:
            semantics = gen_nones(sum(ln))

        semantics = np.array(semantics, dtype=np.int32)
        return Surface(v, n, semantics)

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

    def export(self):
        primitive = self.export_into(FacetModel())
        primitive.buffers.normals.data = self.normals
        return primitive
