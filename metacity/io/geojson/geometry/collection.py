from typing import List
from metacity.io.geojson.geometry.polygon import GJMultiPolygon, GJPolygon
from metacity.io.geojson.geometry.lines import GJLine, GJMultiLine
from metacity.io.geojson.geometry.points import GJMultiPoint, GJPoint
from metacity.io.geojson.geometry.base import GJGeometryObject, GJModelObject
import numpy as np


def parse_geometry(data) -> GJGeometryObject:
    if data is None:
        return None

    type: str = data["type"].lower()

    if type == "point":
        return GJPoint(data)
    elif type == "multipoint":
        return GJMultiPoint(data)
    elif type == "linestring":
        return GJLine(data)
    elif type == "multilinestring":
        return GJMultiLine(data)
    elif type == "polygon":
        return GJPolygon(data)
    elif type == "multipolygon":
        return GJMultiPolygon(data)
    elif type == "geometrycollection":
        return GJGeometryCollection(data)
    return None


class GJGeometryCollection(GJGeometryObject):
    def __init__(self, data):
        super().__init__(data)
        self.geometries = self.parse_geometries()

    def __repr__(self):
        return f"<GeometryCollection: {[f for f in self.geometries]}>"

    @property
    def vertices(self):
        if len(self.geometries) == 0:
            return np.array([])
        vertices = [geometry.vertices for geometry in self.geometries]
        return np.concatenate(vertices, axis=0)

    def parse_geometries(self):
        parsed: List[GJGeometryObject] = []
        if "geometries" in self.data and self.data["geometries"] is not None: 
            for obj in self.data["geometries"]:
                geo = parse_geometry(obj)
                if geo != None:
                    parsed.append(geo)
        return parsed

    def to_primitives(self, shift):
        primitives: List[GJModelObject] = []
        for geometry in self.geometries:
            for g in geometry.to_primitives(shift):
                primitives.append(g)
        return primitives

