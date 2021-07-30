from metacity.helpers.encoding import npfloat32_to_buffer, npint32_to_buffer, base64_to_float32, base64_to_int32
import numpy as np

class NonFacetModel:
    def __init__(self):
        self.vertices = []
        self.semantics = []
        self.semantics_meta = []

    @property
    def exists(self):
        return len(self.vertices) > 0


    def consolidate(self):
        self.vertices = np.array(self.vertices).flatten() 
        self.semantics = np.array(self.semantics).flatten()


    def join_model(self, model):
        self.vertices.extend(model.vertices)
        start_idx = len(self.semantics_meta)
        self.semantics_meta.extend(model.semantics_meta)
        self.semantics.extend(np.array(model.semantics) + start_idx)


    def serialize(self):
        data = {
            'vertices': npfloat32_to_buffer(self.vertices),
            'semantics': npint32_to_buffer(self.semantics),
            'semantics_meta': self.semantics_meta
        }

        return data


    def deserialize(self, data):
        self.vertices = base64_to_float32(data['vertices'])
        self.semantics = base64_to_int32(data['semantics'])
        self.semantics_meta = data['semantics_meta']




class FacetModel(NonFacetModel):
    def __init__(self):
        super().__init__()
        self.normals = []


    def consolidate(self):
        super().consolidate()
        self.normals = np.array(self.normals).flatten()


    def join_model(self, model):
        super().join_model(model)
        self.normals.extend(model.normals)


    def serialize(self):
        data = super().serialize()
        data['normals'] =  npfloat32_to_buffer(self.normals)
        return data


    def deserialize(self, data):
        super().deserialize(data)
        self.normals = base64_to_float32(data['normals'])
