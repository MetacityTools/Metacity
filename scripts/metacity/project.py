from metacity.geometry.bbox import bboxes_bbox
import shutil
import os

import numpy as np

from metacity.helpers.dirtree import LayerDirectoryTree
from metacity.helpers.file import write_json, read_json
from metacity.models.object import MetacityObject


class MetacityConfig:
    def __init__(self, dirtree: LayerDirectoryTree):
        self.shift = [0., 0., 0.]
        try:
            self.deserialize(read_json(dirtree.config))
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


    def export(self, dirtree: LayerDirectoryTree):
        write_json(dirtree.config, self.serialize())



class MetacityLayer:
    def __init__(self, name: str, project_dir: str, load_existing=True):
        self.name = name
        self.dirtree = LayerDirectoryTree(name, project_dir)
        self.dirtree.recreate_layer(load_existing)


    def update_config(self, vertices):
        config = MetacityConfig(self.dirtree)
        if self.empty:
            config.update(vertices)
        config.apply(vertices)
        config.export(self.dirtree)

    
    def apply_config(self, vertices):
        config = MetacityConfig(self.dirtree)
        if self.empty:
            return vertices
        return config.apply(vertices)
            

    @property
    def empty(self):
        return not self.dirtree.any_object_exists


    @property
    def objects(self):
        for oid in self.dirtree.object_ids:
            obj = MetacityObject()
            obj.load_base(oid, self.dirtree)
            yield obj


    def lod_bbox(self, lod):
        return bboxes_bbox([ object.lod_bbox(lod) for object in self.objects ])
            

    @property
    def bbox(self):
        return bboxes_bbox([ object.bbox for object in self.objects ])

    
        



class MetacityProject:
    def __init__(self, directory: str, load_existing=True):
        self.dir = directory
        if os.path.exists(self.dir): 
            if not load_existing:
                shutil.rmtree(self.dir)
        else:
            os.mkdir(self.dir)


    def layer(self, layer_name: str, load_existing=True):        
        layer = MetacityLayer(layer_name, self.dir, load_existing)
        return layer


    @property
    def layers(self):
        dirs = LayerDirectoryTree.layer_dirs(self.dir)
        return [ MetacityLayer(d, self.dir) for d in dirs ]

    

