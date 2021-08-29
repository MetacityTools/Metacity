from metacity.datamodel.models.set import ModelSet
from metacity.dirtree import base as tree
from metacity.helpers.file import read_json, write_json


class MetacityObject:
    def __init__(self):
        self.models = ModelSet()
        self.meta = None
        self.oid = None


    def consolidate(self):
        self.models.consolidate()

    
    def load(self, oid: str, geometry_path: str, meta_path: str):
        self.oid = oid
        self.models.load(oid, geometry_path)
        meta_file = tree.metadata_for_oid(meta_path, self.oid)
        self.meta = read_json(meta_file)


    def export(self, geometry_path: str, meta_path=""):
        self.models.export(self.oid, geometry_path)
        self.__export_meta(meta_path)


    def __export_meta(self, meta_path):
        if meta_path != "":
            meta_file = tree.metadata_for_oid(meta_path, self.oid)
            write_json(meta_file, self.meta)
