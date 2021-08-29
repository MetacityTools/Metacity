from metacity.datamodel.layer.config import LayerConfig
from metacity.datamodel.object import MetacityObject
from metacity.dirtree import base as tree
from metacity.utils.base.bbox import bboxes_bbox


class MetacityLayer:
    def __init__(self, layer_dir: str, load_existing=True):
        self.dir = layer_dir
        tree.recreate_layer(layer_dir, load_existing)


    def update_config(self, vertices): #TODO refactor config stuff
        config = LayerConfig(self.dir)
        if self.empty:
            config.update(vertices)
        config.apply(vertices)
        config.export(self.dir)

    
    def apply_config(self, vertices):
        config = LayerConfig(self.dir)
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
