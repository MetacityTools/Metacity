from metacity.datamodel.buffers.buffer import MetacityBuffer
import numpy as np
from metacity.utils import encoding as en


class Int32Buffer(MetacityBuffer):
    def __init__(self):
        self.data = np.array([], dtype=np.int32)

    def join(self, buffer):
        self.data = np.append(self.data, buffer.data)

    def serialize(self):
        return en.npint32_to_buffer(self.data)

    def deserialize(self, data):
        self.data = en.base64_to_int32(data)

    def __len__(self):
        return len(self.data)

    def deepcopy(self):
        copy = Int32Buffer()
        copy.data = np.copy(self.data)
        return copy

    def erase(self):
        self.data = np.array([], dtype=np.int32)