from metacity.datamodel.buffers.int32 import Int32Buffer
from metacity.datamodel.primitives.base import BaseModel
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

    def add_model(self, oid_id: int, amodel: BaseModel):
        self.add_oid_buffer_to_model(oid_id, amodel)
        for model in self.models:
            if model.TYPE == amodel.TYPE:
                model.join(amodel)
                return
        # in case the type is not present in tile already
        self.models.append(amodel.deepcopy)

    def add_oid_buffer_to_model(self, oid_id, amodel):
        idbuffer = Int32Buffer()
        idbuffer.set(np.array([oid_id] * len(amodel.buffers.semantics), dtype=np.int32))
        amodel.buffers["oid"] = idbuffer

    def export(self, grid_dir):
        super().export(self.name, fs.grid_tiles_dir(grid_dir))
        tile_config = fs.tile_config(grid_dir, self.name)
        write_json(tile_config, self.serialize())

    def delete(self, grid_dir):
        super().delete(self.name, fs.grid_tiles_dir(grid_dir))
        tile_config = fs.tile_config(grid_dir, self.name)
        fs.base.remove_file(tile_config)

    def add_object_to_cache(self, grid_dir, oid: str, models: ModelSet):
        cache_dir = fs.tile_cache_dir(grid_dir, self.name)
        models.export(oid, cache_dir)
        
    def cache_objects(self, grid_dir):
        cache_dir = fs.tile_cache_dir(grid_dir, self.name)
        return fs.base.objects(cache_dir)  

    def delete_object_from_cache(self, grid_dir, oid: str):
        cache_dir = fs.tile_cache_dir(grid_dir, self.name)
        models = ModelSet()
        models.delete(oid, cache_dir)

    def contains_object(self, grid_dir, oid: str):
        return fs.tile_cache_object_exists(grid_dir, self.name, oid)



