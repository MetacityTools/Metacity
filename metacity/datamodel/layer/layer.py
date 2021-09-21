from metacity.datamodel.layer.config import LayerConfig
from metacity.datamodel.object import MetacityObject
from metacity.filesystem import layer as fs
from metacity.utils.bbox import bboxes_bbox
import uuid


class MetacityLayer:
    def __init__(self, layer_dir: str, load_existing=True):
        self.dir = layer_dir
        fs.recreate_layer(layer_dir, load_existing)

    @property
    def config(self):
        return LayerConfig(self)

    @property
    def empty(self):
        return not fs.any_object_in_layer(self.dir)

    @property
    def bbox(self):
        return bboxes_bbox([object.models.bbox for object in self.objects])

    @property
    def geometry_path(self):
        return fs.layer_geometry(self.dir)

    @property
    def cache_path(self):
        return fs.layer_cache(self.dir)

    @property
    def meta_path(self):
        return fs.layer_metadata(self.dir)

    @property
    def objects(self):
        gp = self.geometry_path
        mp = self.meta_path
        for oid in fs.layer_objects(self.dir):
            obj = MetacityObject()
            obj.load(oid, gp, mp)
            yield obj

    def object(self, oid):
        gp = self.geometry_path
        mp = self.meta_path
        obj = MetacityObject()
        obj.load(oid, gp, mp)
        return obj

    @property
    def object_names(self):
        return [oid for oid in fs.layer_objects(self.dir)]

    def add_object(self, object: MetacityObject):
        object.export(self.geometry_path, self.meta_path)

    def delete_object(self, oid):
        gp = self.geometry_path
        mp = self.meta_path
        obj = MetacityObject()
        obj.oid = oid
        obj.delete(gp, mp)

    def generate_oid(self):
        names = self.object_names
        oid = str(uuid.uuid4())
        while oid in names:
            oid = str(uuid.uuid4())
        return oid