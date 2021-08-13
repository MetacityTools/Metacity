import numpy as np

from metacity.geometry.bbox import bboxes_bbox
from metacity.helpers.dirtree import layer as tree
from metacity.helpers.file import read_json, write_json
from metacity.models.object import MetacityObject


class MetacityConfig:
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



class MetacityLayer:
    def __init__(self, layer_dir: str, load_existing=True):
        self.dir = layer_dir
        tree.recreate_layer(layer_dir, load_existing)


    def update_config(self, vertices):
        config = MetacityConfig(self.dir)
        if self.empty:
            config.update(vertices)
        config.apply(vertices)
        config.export(self.dir)

    
    def apply_config(self, vertices):
        config = MetacityConfig(self.dir)
        if self.empty:
            return vertices
        return config.apply(vertices)
            

    @property
    def empty(self):
        return not tree.any_object_in_layer(self.dir)


    @property
    def objects(self):
        gp = self.geometry_path
        mp = self.meta_path
        for oid in tree.layer_objects(self.dir):
            obj = MetacityObject()
            obj.load(oid, gp, mp)
            yield obj


    def add_object(self, object: MetacityObject):
        object.export(self.geometry_path, self.meta_path)


    def lod_bbox(self, lod):
        return bboxes_bbox([ object.lod_bbox(lod) for object in self.objects ])
            

    @property
    def bbox(self):
        return bboxes_bbox([ object.bbox for object in self.objects ])


    @property
    def geometry_path(self):
        return tree.layer_geometry(self.dir)


    @property
    def cache_path(self):
        return tree.layer_cache(self.dir)


    @property
    def meta_path(self):
        return tree.layer_metadata(self.dir)



class MetacityProject:
    def __init__(self, directory: str, load_existing=True):
        self.dir = directory
        tree.recrete_project(self.dir, load_existing)


    def layer(self, layer_name: str, load_existing=True):  
        layer_dir = tree.layer_dir(self.dir, layer_name)   
        layer = MetacityLayer(layer_dir, load_existing)
        return layer


    @property
    def layer_names(self):
        return tree.layer_names(self.dir)


    @property
    def layers(self):
        dirs = self.layer_names
        return [ MetacityLayer(d, self.dir) for d in dirs ]


    

