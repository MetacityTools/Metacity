import numpy as np
from metacity.filesystem import layer as fs
from metacity.filesystem.file import read_json, write_json


class LayerConfig:
    def __init__(self, layer_dir):
        self.shift = [0., 0., 0.]
        try:
            path = fs.layer_config(layer_dir)
            self.deserialize(read_json(path))
        except Exception as e:
            print(e)

    def apply(self, layer, vertices):
        if layer.empty:
            self.shift = np.amin(vertices, axis=0).tolist()
            self.export(layer.dir)
        vertices -= self.shift

    def serialize(self):
        return {
            'shift': self.shift
        }

    def deserialize(self, data):
        self.shift = data['shift']

    def export(self, layer_dir):
        path = fs.layer_config(layer_dir)
        write_json(path, self.serialize())
