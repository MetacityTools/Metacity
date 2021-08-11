from typing import Dict

import numpy as np
from metacity.helpers.dirtree import LayerDirectoryTree
from metacity.helpers.file import write_json, read_json


class MetaTile:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.bbox = np.array([0, 0, 0])


    def load(self, dirtree: LayerDirectoryTree, x, y):
        self.deserialize(read_json(dirtree.tile_config(x, y)))


    def serialize(self):
            return {
                'x': self.x,
                'y': self.y,
                'bbox': self.bbox.tolist(),
            }


    def deserialize(self, data):
        self.x = data['x']
        self.y = data['y']
        self.bbox = np.array(data['bbox'])


    def export(self, dirtree: LayerDirectoryTree):
        write_json(dirtree.tile_config(self.x, self.y), self.serialize())

