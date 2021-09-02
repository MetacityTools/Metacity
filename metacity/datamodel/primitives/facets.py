from metacity.datamodel.primitives.base import BaseModel
from metacity.utils import encoding as en
from metacity.datamodel.buffers.float32 import Float32Buffer
import numpy as np



class FacetModel(BaseModel):
    TYPE = "facets"

    def __init__(self):
        super().__init__()
        self.buffers.normals = Float32Buffer()

    @property
    def items(self):
        vert = self.buffers.vertices.reshape((self.buffers.vertices.shape[0] // 9, 3, 3))
        norm = self.buffers.normals.reshape((self.buffers.normals.shape[0] // 9, 3, 3))
        sema = self.buffers.semantics.reshape((self.buffers.semantics.shape[0] // 3, 3))

        for triangle, normal, semantic in zip(vert, norm, sema):
            yield triangle, normal, semantic

    @property
    def slicer(self):
        # TODO
        pass

