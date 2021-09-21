from metacity.io.geojson.geometry.base import GJModelObject
from metacity.datamodel.primitives.lines import LineModel
import numpy as np


class GJLine(GJModelObject):
    def __init__(self, data):
        super().__init__(data)

    def to_primitives(self, shift):
        if self.empty:
            return []
        model = LineModel()
        vertices = self.prep_coords() - shift
        model.buffers.vertices.set(vertices.flatten())
        nvert = model.buffers.vertices.shape[0] // 3
        model.buffers.semantics.set(self.empty_semantics(nvert))
        return [model]

    def prep_coords(self):
        return np.repeat(self.coordinates, 2, axis=0)[1:-1]


class GJMultiLine(GJLine):
    def __init__(self, data):
        super().__init__(data)

    def prep_coords(self):
        verts = []
        for linestring in self.coordinates:
            verts.append(np.repeat(linestring, 2, axis=0)[1:-1])
        return np.concatenate(verts, dtype=np.float32)