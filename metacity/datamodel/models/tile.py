from metacity.filesystem.file import read_json, write_json
from metacity.datamodel.models.set import ModelSet
from metacity.filesystem import grid as fs
import numpy as np


class MetaTile(ModelSet):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.tile_bbox = np.array([0, 0, 0])
        self.object_count = 0

    @property
    def bbox(self):
        return self.tile_bbox

    @bbox.setter
    def bbox(self, bbox):
        self.tile_bbox = bbox

    @property
    def name(self):
        return fs.tile_name(self.x, self.y)

    def serialize(self):
        return {
            'x': self.x,
            'y': self.y,
            'bbox': self.bbox.tolist(),
            'object_count': self.object_count
        }

    def deserialize(self, data):
        self.x = data['x']
        self.y = data['y']
        self.bbox = np.array(data['bbox'])
        self.object_count = data['object_count']

    def load(self, grid_dir, tile_name):
        tile_config = fs.tile_config(grid_dir, tile_name)
        tile_dir = fs.grid_tiles_dir(grid_dir)
        super().load(tile_name, tile_dir)
        self.deserialize(read_json(tile_config))

    def export(self, grid_dir):
        super().export(self.name, fs.grid_tiles_dir(grid_dir))
        tile_config = fs.tile_config(grid_dir, self.name)
        write_json(tile_config, self.serialize())
