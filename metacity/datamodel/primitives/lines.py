import numpy as np
from metacity.datamodel.primitives.base import BaseModel
from metacity.utils.slicing import split_line
import numpy as np


class LineModel(BaseModel):
    TYPE = "lines"

    def __init__(self):
        super().__init__()

    @property
    def items(self):
        vert = self.buffers.vertices.reshape((self.buffers.vertices.shape[0] // 6, 2, 3))
        sema = self.buffers.semantics.reshape((self.buffers.semantics.shape[0] // 2, 2))

        for segment, semantic in zip(vert, sema):
            yield segment, semantic

    @property
    def deepcopy(self):
        model = LineModel()
        self.deepcopy_into(model)
        return model

    def split(self, x_planes, y_planes):
        vertices, semantics = [], []
        for segment, semantic in self.items:
            segments = split_line(segment, x_planes, y_planes)
            vertices.extend(segments)
            semantics.extend(np.repeat([semantic], len(segments), axis=0))
        vertices = np.array(vertices, dtype=np.float32).flatten()
        semantics = np.array(semantics, dtype=np.int32).flatten()

        splitted = LineModel()
        self.deepcopy_nonbuffers(splitted)
        splitted.buffers.vertices.set(vertices)
        splitted.buffers.semantics.set(semantics)
        return splitted



