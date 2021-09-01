from metacity.datamodel.primitives.base import BaseModel


class PointModel(BaseModel):
    TYPE = "points"

    def __init__(self):
        super().__init__()

    @property
    def items(self):
        vert = self.vertices.reshape((self.vertices.shape[0] // 3, 3))
        sema = self.semantics

        for segment, semantic in zip(vert, sema):
            yield segment, semantic

    @property
    def slicer(self):
        # TODO
        pass

    @property
    def joiner(self):
        # TODO
        pass

    def serialize(self):
        data = super().serialize()
        return data
