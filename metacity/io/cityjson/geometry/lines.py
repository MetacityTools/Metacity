import numpy as np
from metacity.datamodel.primitives.lines import LineModel
from metacity.io.cityjson.geometry.base import (CJBasePrimitive, gen_nones,
                                                rep_nones)


class CJLines(CJBasePrimitive):
    def __init__(self, data, vertices):
        super().__init__(data)
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
        if semantics["values"] is not None:
            buffer = rep_nones(semantics["values"])
            buffer = np.repeat(buffer, segment_lengths)
        else:
            buffer = gen_nones(sum(segment_lengths))

        self.semantics = np.array(buffer, dtype=np.int32)
        self.meta = semantics["surfaces"]

    def export(self):
        return self.export_into(LineModel())
