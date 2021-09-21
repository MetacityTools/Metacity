import numpy as np
from metacity.filesystem import layer as fs
from metacity.filesystem.file import read_json, write_json


class LayerConfig:
    def __init__(self, layer):
        self.shift = [0., 0., 0.]
        self.layer = layer
        try:
            path = fs.layer_config(layer.dir)
            self.deserialize(read_json(path))
        except Exception as e:
            print(e)

    def apply(self, vertices):
        if self.layer.empty:
            self.shift = np.amin(vertices, axis=0).tolist()
            self.export()
        vertices -= self.shift

    def serialize(self):
        return {
            'shift': self.shift
        }

    def deserialize(self, data):
        self.shift = data['shift']

    def export(self):
        path = fs.layer_config(self.layer.dir)
        write_json(path, self.serialize())
