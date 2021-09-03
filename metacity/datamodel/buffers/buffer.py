import numpy as np


class MetacityBuffer:
    def __init__(self):
        self.data = np.array([])

    def join(self, buffer):
        raise NotImplementedError("Method join not implemented")

    def serialize(self):
        raise NotImplementedError("Method serialize not implemented")

    def deserialize(self):
        raise NotImplementedError("Method deserialize not implemented")

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        return self.data == other.data

    @property
    def shape(self):
        return self.data.shape

    def reshape(self, shape):
        return self.data.reshape(shape)

    def set(self, data):
        self.data = data

    def deepcopy(self):
        copy = MetacityBuffer()
        copy.data = np.copy(self.data)
        return copy

    def erase(self):
        self.data = np.array([])