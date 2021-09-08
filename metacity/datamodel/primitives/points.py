from metacity.utils.sorter import GridSorter
from metacity.datamodel.primitives.base import BaseModel

class PointModel(BaseModel):
    TYPE = "points"

    def __init__(self):
        super().__init__()

    @property
    def items(self):
        vert = self.buffers.vertices.reshape((self.buffers.vertices.shape[0] // 3, 3))
        sema = self.buffers.semantics.data

        for point, semantic in zip(vert, sema):
            yield point, semantic

    @property
    def deepcopy(self):
        model = PointModel()
        self.deepcopy_into(model)
        return model

    @property
    def deepcopy_nobuffers(self):
        model = PointModel()
        self.deepcopy_into_nobuffers(model)
        return model

    def split(self, x_planes, y_planes):
        return self.__splitsort(x_planes, y_planes)

    def __splitsort(self, x_planes, y_planes):
        grid = GridSorter(x_planes, y_planes)
        for p, s in self.items:
            grid.insert((p, s), p)
        models = []
        for elements in grid.partitions.values():
            seg, sem = [], []
            for element in elements:
                seg.append(element[0])
                sem.append(element[1])
            model = PointModel()
            self.set_meta_copy(model, seg, sem)
            models.append(model)
        return models

