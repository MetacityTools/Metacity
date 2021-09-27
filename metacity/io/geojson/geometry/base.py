import numpy as np


class GJObject:
    def __init__(self, data):
        self.data = data


class GJGeometryObject(GJObject):
    def __init__(self, data):
        super().__init__(data)

    def to_primitives(self, shift):
        raise NotImplementedError("Method to_primitives() not implemented")


class GJModelObject(GJGeometryObject):
    def __init__(self, data):
        super().__init__(data)
        self.coordinates = self.format_coords()

    @property
    def empty(self):
        return len(self.coordinates) == 0

    def to_3d(self, data):
        data = np.array(data, dtype=np.float32)
        if data.shape[-1] == 2:
            pads = [(0, 0)] * (data.ndim - 1)
            pads.append((0, 1))
            data = np.pad(data, pads)
        if data.shape[-1] != 3:
            raise Exception(f"Coordinate data have an unexpected shape: {data.shape}")
        return data

    def format_coords(self):
        if self.data["coordinates"] is None:
            return []
        return self.data["coordinates"]

    def empty_semantics(self, nvert):
        return np.array([-1] * nvert, dtype=np.int32)

    @property
    def flatten_vertices(self):
        raise NotImplementedError()

    @property
    def vertices(self):
        if self.empty:
            return np.array([])
        v = self.flatten_vertices
        return v.reshape((len(v) // 3, 3))

            