import numpy as np
from metacity.filesystem import layer as fs
from metacity.filesystem.file import read_json, write_json


class LayerConfig:
    def __init__(self, layer_dir):
        self.shift = [0., 0., 0.]
        try:
            path = fs.layer_config(layer_dir)
            self.deserialize(read_json(path))
        except:
            pass


    def serialize(self):
        return {
            'shift': self.shift
        }


    def deserialize(self, data):
        self.shift = data['shift']


    def apply(self, vertices):
        vertices -= self.shift


    def update(self, vertices):
        self.shift = np.amin(vertices, axis=0).tolist()


    def export(self, layer_dir):
        path = fs.layer_config(layer_dir)
        write_json(path, self.serialize())
