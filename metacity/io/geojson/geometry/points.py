from metacity.io.geojson.geometry.base import GJModelObject
from metacity.datamodel.primitives.points import PointModel
import numpy as np

class GJPoint(GJModelObject):
    def __init__(self, data):
        super().__init__(data)
        self.coordinates = self.to_3d(self.coordinates)

    def to_primitives(self, shift):
        if self.empty:
            return []
        model = PointModel()
        vertices = self.coordinates - shift
        model.buffers.vertices.set(vertices.flatten())
        nvert = model.buffers.vertices.shape[0] // 3
        model.buffers.semantics.set(self.empty_semantics(nvert))
        return [model]

    @property
    def flatten_vertices(self):
        return np.array(self.coordinates).flatten()


class GJMultiPoint(GJPoint):
    def __init__(self, data):
        super().__init__(data)

