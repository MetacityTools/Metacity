import numpy as np
from metacity.utils import encoding as en
from metacity.utils.bbox import empty_bbox, vertices_bbox


class BaseModel:
    TYPE = "base"

    def __init__(self):
        """
        Initializes empy instance of Base Model.
        This class should not be instantiated on its own.
        """
        self.vertices = np.array([], dtype=np.float32)
        self.semantics = np.array([], dtype=np.int32)
        self.modelid = None
        self.meta = []
        self.tags = {}

    @property
    def exists(self):
        """
        Returns True if the model contains any vertices,
        otherwise returns False.
        """
        return len(self.vertices) > 0

    @property
    def empty(self):
        """
        Returns True if the model contains no vertices,
        otherwise returns False.
        """
        return len(self.vertices) == 0

    @property
    def has_semantics(self):
        """
        Returns True if the model contains semantic information,
        otherwise returns False.
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

    def join(self, model):
        self.vertices = np.append(self.vertices, model.vertices)
        semantics = self.__update_semantics(model.semantics)
        self.semantics = np.append(self.semantics, semantics)
        self.meta.extend(model.meta)
        if self.modelid and model.modelid:
            self.modelid = np.append(self.modelid, model.modelid)

    def __update_semantics(self, semantics):
        start_idx = len(self.meta)
        semantics[semantics == -1] -= start_idx
        semantics += start_idx
        return semantics

    def serialize(self):
        data = {
            'vertices': en.npfloat32_to_buffer(self.vertices),
            'semantics': en.npint32_to_buffer(self.semantics),
            'meta': self.meta,
            'tags': self.tags,
            'type': self.TYPE
        }
        if self.modelid is not None:
            data['modelid'] = en.npint32_to_buffer(self.modelid)
        return data

    def deserialize(self, data):
        self.vertices = en.base64_to_float32(data['vertices'])
        self.semantics = en.base64_to_int32(data['semantics'])
        self.meta = data['meta']
        self.tags = data['tags']
        if 'modelid' in data:
            self.modelid = en.base64_to_int32(data['modelid'])
