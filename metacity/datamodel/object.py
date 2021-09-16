from metacity.datamodel.models.set import ModelSet
from metacity.filesystem import base as fs
from metacity.filesystem.file import read_json, write_json


class MetacityObject:
    def __init__(self):
        self.models = ModelSet()
        self.meta = None
        self.oid = None

    def load(self, oid: str, geometry_path: str, meta_path: str):
        self.oid = oid
        self.models.load(oid, geometry_path)
        meta_file = fs.metadata_for_oid(meta_path, self.oid)
        self.meta = read_json(meta_file)

    def export(self, geometry_path: str, meta_path=""):
        self.models.export(self.oid, geometry_path)
        self.__export_meta(meta_path)

    def delete(self, geometry_path: str, meta_path: str):
        meta_file = fs.metadata_for_oid(meta_path, self.oid)
        fs.remove_file(meta_file)
        self.models.delete(self.oid, geometry_path)

    def __export_meta(self, meta_path):
        if meta_path != "":
            meta_file = fs.metadata_for_oid(meta_path, self.oid)
            write_json(meta_file, self.meta)
