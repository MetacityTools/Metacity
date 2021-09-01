import numpy as np
from metacity.datamodel.primitives.points import PointModel
from metacity.io.cityjson.geometry.base import (CJBasePrimitive, gen_nones,
                                                rep_nones)


class CJPoints(CJBasePrimitive):
    def __init__(self, data, vertices):
        super().__init__(data)
        self.vertices = self.parse_vertices(data, vertices)
        elements_count = len(self.vertices) // 3

        if "semantics" in data:
            self.parse_semantics(data["semantics"], elements_count)
        else:
            self.generate_semantics(elements_count)

    def parse_vertices(self, data, vertices):
        return np.array(vertices[data["boundaries"]],
                        dtype=np.float32).flatten()

    def parse_semantics(self, semantics, elements_count):
        if semantics["values"] is not None:
            buffer = rep_nones(semantics["values"])
        else:
            buffer = gen_nones(elements_count)

        self.semantics = np.array(buffer, dtype=np.int32)
        self.meta = semantics["surfaces"]

    def export(self):
        return self.export_into(PointModel())
