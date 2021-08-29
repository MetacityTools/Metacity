from metacity.datamodel.models.primitives.base import BaseModel
from metacity.utils.base import encoding as en
import numpy as np

class FacetModel(BaseModel):
    TYPE = "facets"


    def __init__(self):
        super().__init__()
        self.normals = np.array([])


    @property
    def items(self):
        vert = self.vertices.reshape((self.vertices.shape[0] // 9, 3, 3))
        norm = self.normals.reshape((self.normals.shape[0] // 9, 3, 3))
        sema = self.semantics.reshape((self.semantics.shape[0] // 3, 3))

        for triangle, normal, semantic in zip(vert, norm, sema):
            yield triangle, normal, semantic


    @property
    def slicer(self):
        pass #TODO


    @property
    def joiner(self):
        pass #TODO


    def serialize(self):
        data = super().serialize()
        data['normals'] =  en.npfloat32_to_buffer(self.normals)
        data['type'] = FacetModel.TYPE
        return data


    def deserialize(self, data):
        super().deserialize(data)
        self.normals = en.base64_to_float32(data['normals'])



