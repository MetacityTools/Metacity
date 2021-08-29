import numpy as np
from metacity.utils.base import encoding as en
from metacity.utils.base.bbox import empty_bbox, vertices_bbox

class BaseModel:
    TYPE = "base"

    def __init__(self):
        """
        Initializes empy instance of Base Model. This class should not be instantiated on its own.
        """
        self.vertices = np.array([], dtype=np.float32)
        self.semantics = np.array([], dtype=np.int32)
        self.semantics_meta = []


    @property
    def exists(self):
        """
        Returns True if the model contains any vertices, otherwise returns False.
        """
        return len(self.vertices) > 0

    
    @property
    def empty(self):
        """
        Returns True if the model contains no vertices, otherwise returns False.
        """
        return len(self.vertices) == 0


    @property
    def has_semantics(self):
        """
        Returns True if the model contains semantic information, otherwise returns False.
        """
        return len(self.semantics) > 0


    @property
    def bbox(self):
        if self.empty:
            return empty_bbox()
        vertices = self.vertices.reshape((self.vertices.shape[0] // 3, 3))
        return vertices_bbox(vertices)

    
    @property
    def items(self):
        pass


    @property
    def slicer(self):
        pass


    @property
    def joiner(self):
        pass


    def serialize(self):
        data = {
            'vertices': en.npfloat32_to_buffer(self.vertices),
            'semantics': en.npint32_to_buffer(self.semantics),
            'semantics_meta': self.semantics_meta
        }
        return data


    def deserialize(self, data):
        self.vertices = en.base64_to_float32(data['vertices'])
        self.semantics = en.base64_to_int32(data['semantics'])
        self.semantics_meta = data['semantics_meta']


