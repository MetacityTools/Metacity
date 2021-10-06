from metacity.datamodel.object import Object
from typing import List, Dict
from metacity.io.cityjson.geometry.geometry import CJGeometry


class CJObject:
    def __init__(self, oid: str, data: Dict, vertices, templates):
        self.oid = oid
        self.meta = self.clean_meta(data)
        self.geometry: List[CJGeometry] = self.parse_geometry(data, vertices,
                                                              templates)

    def clean_meta(self, data):
        return {key: value for key, value in data.items()
                if key not in ['geometry', 'semantics']}

    def parse_geometry(self, data, vertices, templates):
        geometry = data['geometry']
        geometries = []
        for geometry_object in geometry:
            geometries.append(CJGeometry(geometry_object, vertices, templates))
        return geometries

    def export(self, geometry_path, meta_path):
        object = Object()
        object.meta = self.meta
        object.oid = self.oid
        for g in self.geometry:
            object.models.models.append(g.export())
        object.export(geometry_path, meta_path)
