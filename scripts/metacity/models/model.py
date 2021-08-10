from metacity.geometry.bbox import empty_bbox, vertices_bbox
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

    
    @property
    def empty(self):
        return len(self.vertices) == 0


    @property
    def has_semantics(self):
        return len(self.semantics) > 0


    def consolidate(self):
        self.vertices = np.array(self.vertices).flatten() 
        self.semantics = np.array(self.semantics).flatten()


    def join_model(self, model, store_semantics_meta = True):
        self.vertices.extend(model.vertices)
        start_idx = len(self.semantics_meta)
        self.semantics.extend(np.array(model.semantics) + start_idx)

        if store_semantics_meta:
            self.semantics_meta.extend(model.semantics_meta)


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


    @property
    def bbox(self):
        if not self.exists:
            return empty_bbox()
        vertices = self.vertices.reshape((self.vertices.shape[0] // 3, 3))
        return vertices_bbox(vertices)


    @property
    def items(self):
        pass



class PointModel(NonFacetModel):
    def __init__(self):
        super().__init__()

    @property
    def items(self):
        self.consolidate()
        vert = self.vertices.reshape((self.vertices.shape[0] // 3, 3))
        sema = self.semantics
        
        for segment, semantic in zip(vert, sema):
            yield segment, semantic



class LineModel(NonFacetModel):
    def __init__(self):
        super().__init__()

    @property
    def items(self):
        self.consolidate()
        vert = self.vertices.reshape((self.vertices.shape[0] // 6, 2, 3))
        sema = self.semantics.reshape((self.semantics.shape[0] // 2, 2))

        for segment, semantic in zip(vert, sema):
            yield segment, semantic



class FacetModel(NonFacetModel):
    def __init__(self):
        super().__init__()
        self.normals = []


    def consolidate(self):
        super().consolidate()
        self.normals = np.array(self.normals).flatten()


    def join_model(self, model, store_semantics_meta = True):
        super().join_model(model, store_semantics_meta)
        self.normals.extend(model.normals)


    def serialize(self):
        data = super().serialize()
        data['normals'] =  npfloat32_to_buffer(self.normals)
        return data


    def deserialize(self, data):
        super().deserialize(data)
        self.normals = base64_to_float32(data['normals'])


    @property
    def items(self):
        self.consolidate()
        vert = self.vertices.reshape((self.vertices.shape[0] // 9, 3, 3))
        norm = self.normals.reshape((self.normals.shape[0] // 9, 3, 3))
        sema = self.semantics.reshape((self.semantics.shape[0] // 3, 3))

        for triangle, normal, semantic in zip(vert, norm, sema):
            yield triangle, normal, semantic



class TileModel:
    def __init__(self, primitive_class):
        self.primitive = primitive_class()
        self.idbuffer = []
        self.semantics_meta = {}


    def consolidate(self):
        self.primitive.consolidate()
        self.idbuffer = np.array(self.idbuffer).flatten()


    def join_primitive_model(self, model, bid):
        self.primitive.join_model(model, store_semantics_meta=False)
        count_vertices = model.vertices.shape[0] // 3 #vertices are always present
        self.idbuffer.extend(np.full((count_vertices,), bid))
        self.semantics_meta[bid] = model.semantics_meta
        
        
    def serialize(self):
        data = self.primitive.serialize()
        data['idbuffer'] = npint32_to_buffer(self.idbuffer)
        return data


