from metacity.io.cityjson.geometry.base import CJBasePrimitive, rep_nones, gen_nones
import numpy as np


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
        return np.array(vertices[data["boundaries"]], dtype=np.float32).flatten()


    def parse_semantics(self, semantics, elements_count):
        if semantics["values"] != None:
            buffer = rep_nones(semantics["values"])
        else:
            buffer = gen_nones(elements_count)

        self.semantics = np.array(buffer, dtype=np.int32)
        self.meta = semantics["surfaces"]


    def transform(self):
        pass #TODO