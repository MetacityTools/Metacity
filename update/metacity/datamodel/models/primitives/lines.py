from metacity.datamodel.models.primitives.base import BaseModel


class LineModel(BaseModel):
    TYPE = "lines"


    def __init__(self):
        super().__init__()


    @property
    def items(self):
        vert = self.vertices.reshape((self.vertices.shape[0] // 6, 2, 3))
        sema = self.semantics.reshape((self.semantics.shape[0] // 2, 2))

        for segment, semantic in zip(vert, sema):
            yield segment, semantic


    @property
    def slicer(self):
        pass #TODO


    @property
    def joiner(self):
        pass #TODO


    def serialize(self):
        data = super().serialize()
        data['type'] = LineModel.TYPE
        return data