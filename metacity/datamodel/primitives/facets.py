from metacity.utils.slicing import split_triangle
from metacity.datamodel.primitives.base import BaseModel
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
    def deepcopy(self):
        model = FacetModel()
        self.deepcopy_into(model)
        return model

    def split(self, x_planes, y_planes):
        vertices, normals, semantics = [], [], []
        for triangle, normal, semantic in self.items:
            triangles = split_triangle(triangle, x_planes, y_planes)
            vertices.extend(triangles)
            normals.extend(np.repeat([normal], len(triangles), axis=0))
            semantics.extend(np.repeat([semantic], len(triangles), axis=0))
        vertices = np.array(vertices, dtype=np.float32).flatten()
        normals = np.array(normals, dtype=np.float32).flatten()
        semantics = np.array(semantics, dtype=np.int32).flatten()

        splitted = FacetModel()
        self.deepcopy_nonbuffers(splitted)
        splitted.buffers.vertices.set(vertices)
        splitted.buffers.normals.set(normals)
        splitted.buffers.semantics.set(semantics)

        return splitted
