from metacity.io.geojson.geometry.base import GJModelObject
from metacity.datamodel.primitives.facets import FacetModel
from metacity.utils.surface import Surface
import numpy as np
from earcut import earcut as ec


class GJPolygon(GJModelObject):
    def __init__(self, data):
        super().__init__(data)

    def triangulate(self, coords):
        data = ec.flatten(coords)
        vs = np.array(data["vertices"])
        normal, normal_exists = ec.normal(vs)
        if not normal_exists:
            return Surface()
        ti = ec.earcut(vs, data["holes"], 3)
        vs.reshape((vs.shape[0] // 3, 3))
        v = np.array(vs[ti], dtype=np.float32)
        tri_count = len(ti)    
        n = np.repeat([normal], tri_count, axis=0).astype(np.float32)    
        s = np.repeat([-1], tri_count, axis=0).astype(np.int32)   
        return Surface(v, n, s)

    def to_primitives(self, shift):
        if self.empty:
            return []
        model = FacetModel()
        vertices = self.coordinates - shift
        surface = self.triangulate(vertices)
        model.buffers.vertices.set(np.array(surface.v, dtype=np.float32))
        model.buffers.vertices.set(np.array(surface.n, dtype=np.float32))
        model.buffers.semantics.set(np.array(surface.s, dtype=np.int32))
        return [model]


class GJMultiPolygon(GJPolygon):
    def __init__(self, data):
        super().__init__(data)

    def triangulate(self, coords):
        s = Surface()
        for surface in coords:
            s.join(super().triangulate(surface))
        return s