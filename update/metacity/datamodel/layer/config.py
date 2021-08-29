import numpy as np
from metacity.dirtree import layer as tree
from metacity.helpers.file import read_json, write_json


class LayerConfig:
    def __init__(self, layer_dir):
        self.shift = [0., 0., 0.]
        try:
            path = tree.layer_config(layer_dir)
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
        return vertices


    def update(self, vertices):
        self.shift = np.amin(vertices, axis=0).tolist()


    def export(self, layer_dir):
        path = tree.layer_config(layer_dir)
        write_json(path, self.serialize())
