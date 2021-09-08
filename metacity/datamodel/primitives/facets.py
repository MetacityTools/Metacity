from metacity.utils.sorter import GridSorter
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

    @property
    def deepcopy_nobuffers(self):
        model = FacetModel()
        self.deepcopy_into_nobuffers(model)
        return model

    def split(self, x_planes, y_planes):
        v, n, s = [], [], []
        for triangle, normal, semantic in self.items:
            triangles = split_triangle(triangle, x_planes, y_planes)
            v.extend(triangles)
            n.extend(np.repeat([normal], len(triangles), axis=0))
            s.extend(np.repeat([semantic], len(triangles), axis=0))
        model = FacetModel()
        self.set_meta_copy(model, v, n, s)
        return model.__splitsort(x_planes, y_planes)

    def __splitsort(self, x_planes, y_planes):
        grid = GridSorter(x_planes, y_planes)
        for t, n, s in self.items:
            center = np.sum(t, axis=0) / 3
            grid.insert((t, n, s), center)
        models = []
        for elements in grid.partitions.values():
            v, n, s = [], [], []
            for element in elements:
                v.append(element[0])
                n.append(element[1])
                s.append(element[2])
            model = FacetModel()
            self.set_meta_copy(model, v, n, s)
            models.append(model)
        return models

    def set_meta_copy(self, model, *data):
        vertices, normals, semantics = data
        super().set_meta_copy(model, vertices, semantics)
        n = np.array(normals, dtype=np.float32).flatten()
        model.buffers.normals.set(n)
