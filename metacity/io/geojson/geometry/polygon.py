from metacity.io.geojson.geometry.base import GJModelObject
from metacity.datamodel.primitives.facets import FacetModel
from metacity.utils.surface import Surface
import numpy as np
from earcut import earcut as ec


class GJPolygon(GJModelObject):
    def __init__(self, data):
        super().__init__(data)
        self.transform_coords()

    def triangulate(self, coords, shift):
        data = ec.flatten(coords)
        v = np.array(data["vertices"])
        v = v.reshape((len(v) // 3, 3))
        vs = (v - shift).flatten()
        
        normal, normal_exists = ec.normal(vs)
        if not normal_exists:
            return Surface()
        
        ti = ec.earcut(vs, data["holes"], 3)
        vs = vs.reshape((vs.shape[0] // 3, 3))

        v = np.array(vs[ti], dtype=np.float32)
        vert_count = len(ti)
        n = np.repeat([normal], vert_count, axis=0).astype(np.float32)    
        s = np.repeat([-1], vert_count, axis=0).astype(np.int32)   
        return Surface(v, n, s)

    def to_primitives(self, shift):
        if self.empty:
            return []
        model = FacetModel()
        surface = self.triangulate(self.coordinates, shift)
        model.buffers.vertices.set(np.array(surface.v, dtype=np.float32).flatten())
        model.buffers.normals.set(np.array(surface.n, dtype=np.float32).flatten())
        model.buffers.semantics.set(np.array(surface.s, dtype=np.int32).flatten())
        return [model]

    def transform_polygon(self, polygon):
        segments = []
        for segment in polygon:
            segments.append(self.to_3d(segment))
        return segments

    def transform_coords(self):
        self.coordinates = self.transform_polygon(self.coordinates)

    def flaten_irregular(self, coords):
        flat = []
        for segment in coords:
            flat.extend(segment)
        return flat

    @property
    def flatten_vertices(self):
        flat = self.flaten_irregular(self.coordinates)
        return np.array(flat).flatten()



class GJMultiPolygon(GJPolygon):
    def __init__(self, data):
        super().__init__(data)

    def triangulate(self, coords, shift):
        s = Surface()
        for surface in coords:
            s.join(super().triangulate(surface, shift))
        return s

    def transform_coords(self):
        polygons = []
        for polygon in self.coordinates:
            polygons.append(super().transform_polygon(polygon))
        self.coordinates = polygons

    @property
    def flatten_vertices(self):
        flat = []
        for polygon in self.coordinates:
            flat.extend(self.flaten_irregular(polygon))
        return np.array(flat).flatten()
