from typing import Callable, Union

import numpy as np
from metacity.helpers.encoding import npint32_to_buffer, base64_to_int32
from metacity.models.model import FacetModel, LineModel, PointModel


class TileModel:
    def __init__(self, primitive_class: Callable[[], Union[PointModel, LineModel, FacetModel]]):
        self.primitive = primitive_class()
        self.idbuffer = []


    @property
    def primitive_type(self):
        return self.primitive.json_type


    @property
    def exists(self):
        return len(self.idbuffer) > 0

    
    @property
    def empty(self):
        return len(self.idbuffer) == 0


    def consolidate(self):
        self.primitive.consolidate()
        self.idbuffer = np.array(self.idbuffer).flatten()


    def join_primitive_model(self, bid, model):
        self.primitive.join_model(model)
        count_vertices = model.vertices.shape[0] // 3 #vertices are always present
        self.idbuffer.extend(np.full((count_vertices,), bid))
    
        
    def serialize(self):
        data = self.primitive.serialize()
        data['idbuffer'] = npint32_to_buffer(self.idbuffer)
        return data


    def deserialize(self, data):
        self.primitive.deserialize(data)
        self.idbuffer = base64_to_int32(data['normals'])




