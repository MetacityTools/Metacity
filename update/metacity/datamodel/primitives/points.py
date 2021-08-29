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
        pass #TODO


    @property
    def joiner(self):
        pass #TODO


    def serialize(self):
        data = super().serialize()
        data['type'] = PointModel.TYPE
        return data
