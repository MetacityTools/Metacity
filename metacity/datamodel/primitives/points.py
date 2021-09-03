from metacity.datamodel.primitives.base import BaseModel


class PointModel(BaseModel):
    TYPE = "points"

    def __init__(self):
        super().__init__()

    @property
    def items(self):
        vert = self.buffers.vertices.reshape((self.buffers.vertices.shape[0] // 3, 3))
        sema = self.buffers.semantics.data

        for segment, semantic in zip(vert, sema):
            yield segment, semantic

    @property
    def deepcopy(self):
        model = PointModel()
        self.deepcopy_into(model)
        return model

    def split(self, x_planes, y_planes):
        return self.deepcopy

