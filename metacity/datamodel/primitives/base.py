from metacity.datamodel.buffers.float32 import Float32Buffer
from metacity.datamodel.buffers.int32 import Int32Buffer
import numpy as np
from metacity.utils import encoding as en
from metacity.utils.bbox import empty_bbox, vertices_bbox
from dotmap import DotMap

class BaseModel:
    TYPE = "base"

    def __init__(self):
        """
        Initializes empy instance of Base Model.
        This class should not be instantiated on its own.
        """
        self.buffers = DotMap()
        self.buffers.vertices = Float32Buffer()
        self.buffers.semantics = Int32Buffer()
        self.meta = []
        self.tags = {}

    @property
    def exists(self):
        """
        Returns True if the model contains any vertices,
        otherwise returns False.
        """
        return len(self.buffers.vertices) > 0

    @property
    def empty(self):
        """
        Returns True if the model contains no vertices,
        otherwise returns False.
        """
        return len(self.buffers.vertices) == 0

    @property
    def has_semantics(self):
        """
        Returns True if the model contains semantic information,
        otherwise returns False.
        """
        return len(self.buffers.semantics) > 0

    @property
    def bbox(self):
        if self.empty:
            return empty_bbox()
        vertices = self.buffers.vertices.reshape((self.buffers.vertices.shape[0] // 3, 3))
        return vertices_bbox(vertices)

    @property
    def items(self):
        pass

    @property
    def slicer(self):
        pass

    def join(self, model):
        for buffer in self.buffers.keys():
            self.buffers[buffer].join(model.buffers[buffer])
        self.__update_semantics(len(model.buffers.semantics))
        
        self.meta.extend(model.meta)
        self.tags = {**self.tags, **model.tags}

    def __update_semantics(self, len_right_semantics):
        start_idx = len(self.meta)
        total_len = len(self.buffers.semantics)
        len_left_semantics = total_len - len_right_semantics 
        slice = self.buffers.semantics.data[len_left_semantics:]
        slice[slice != -1] += start_idx

    def serialize(self):
        data = {
            'buffers': {name: buffer.serialize() for name, buffer in self.buffers.items()},
            'meta': self.meta,
            'tags': self.tags,
            'type': self.TYPE
        }
        return data

    def deserialize(self, data):
        for name, buffer in self.buffers.items():
            buffer.deserialize(data['buffers'][name])
        self.meta = data['meta']
        self.tags = data['tags']

