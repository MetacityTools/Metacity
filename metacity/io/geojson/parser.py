from metacity.utils.filesystem import read_json
from typing import List, Union
from metacity.datamodel.object import Object
from abc import ABC, abstractmethod
import metacity.geometry as mg


def flatten(data):
    return [item for sublist in data for item in sublist]


def flatten_polygon(polygon):
    return [[item for sublist in ring for item in sublist] for ring in polygon]


class GJGeometryObject(ABC):
    def __init__(self):
        self.coordinates = []

    def set_coordinates(self, data):
        if 'coordinates' in data:
            self.coordinates = data['coordinates']

    @abstractmethod
    def to_geometry(self):
        pass

    @property
    def dim(self):
        d = self.coordinates
        while isinstance(d[0], list) or isinstance(d[0], tuple):
            d = d[0]
        d = len(d)
        if d < 2 and d > 3:
            raise Exception(
                f"Encountered primitive with unsupported dimension {d}")
        return d


class GJPoint(GJGeometryObject):
    def __init__(self):
        super().__init__()

    def parse(self, data):
        self.set_coordinates(data)

    def to_geometry(self):
        geometry = mg.MultiPoint()
        if self.dim == 2:
            geometry.push_p2(self.coordinates)
        elif self.dim == 3:
            geometry.push_p3(self.coordinates)
        return [geometry.transform()]


class GJMultiPoint(GJPoint):
    def __init__(self):
        super().__init__()

    def to_geometry(self):
        geometry = mg.MultiPoint()
        if self.dim == 2:
            geometry.push_p2(flatten(self.coordinates))
        elif self.dim == 3:
            geometry.push_p3(flatten(self.coordinates))
        return [geometry.transform()]


class GJLine(GJGeometryObject):
    def __init__(self):
        super().__init__()

    def parse(self, data):
        self.set_coordinates(data)

    def to_geometry(self):
        geometry = mg.MultiLine()
        if self.dim == 2:
            geometry.push_l2(flatten(self.coordinates))
        elif self.dim == 3:
            geometry.push_l3(flatten(self.coordinates))
        return [geometry.transform()]


class GJMultiLine(GJLine):
    def __init__(self):
        super().__init__()

    def to_geometry(self):
        geometry = mg.MultiLine()
        dim = self.dim
        for line in self.coordinates:
            if dim == 2:
                geometry.push_l2(flatten(line))
            elif dim == 3:
                geometry.push_l3(flatten(line))
        return [geometry.transform()]


class GJPolygon(GJGeometryObject):
    def __init__(self):
        super().__init__()

    def parse(self, data):
        self.set_coordinates(data)

    def to_geometry(self):
        geometry = mg.MultiPolygon()
        dim = self.dim
        if dim == 2:
            geometry.push_p2(flatten_polygon(self.coordinates))
        elif dim == 3:
            geometry.push_p3(flatten_polygon(self.coordinates))
        return [geometry.transform()]


class GJMultiPolygon(GJPolygon):
    def __init__(self):
        super().__init__()

    def to_geometry(self):
        geometry = mg.MultiPolygon()
        dim = self.dim
        for polygon in self.coordinates:
            if dim == 2:
                geometry.push_p2(flatten_polygon(polygon))
            elif dim == 3:
                geometry.push_p3(flatten_polygon(polygon))
        return [geometry.transform()]


class GJGeometryCollection(GJGeometryObject):
    def __init__(self):
        super().__init__()
        self.geometries: List[GJGeometryObject] = []

    def to_geometry(self):
        return [g for geometry in self.geometries for g in geometry.to_geometry()]


class GJFeature:
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.geometry: GJGeometryObject = None

    def to_object(self):
        o = Object()
        o.geometry = self.geometry.to_geometry()
        o.meta = self.meta
        return o


class GJFeatureCollection:
    def __init__(self):
        super().__init__()
        self.features: List[GJFeature] = []

    def to_objectlist(self):
        objects = [f.to_object() for f in self.features]
        return objects


def parse_point(data):
    geometry = GJPoint()
    geometry.parse(data)
    return geometry


def parse_multipoint(data):
    geometry = GJMultiPoint()
    geometry.parse(data)
    return geometry


def parse_line(data):
    geometry = GJLine()
    geometry.parse(data)
    return geometry


def parse_multiline(data):
    geometry = GJMultiLine()
    geometry.parse(data)
    return geometry


def parse_polygon(data):
    geometry = GJPolygon()
    geometry.parse(data)
    return geometry


def parse_multipolygon(data):
    geometry = GJMultiPolygon()
    geometry.parse(data)
    return geometry


def parse_geometry_collection(data):
    collection = GJGeometryCollection()
    if "geometries" in data and data["geometries"] is not None:
        for obj in data["geometries"]:
            geo = parse_geometry(obj)
            if geo != None:
                collection.geometries.append(geo)
    return collection


typedict = {
    "point": parse_point,
    "multipoint": parse_multipoint,
    "linestring": parse_line,
    "multilinestring": parse_multiline,
    "polygon": parse_polygon,
    "multipolygon": parse_multipolygon,
    "geometrycollection": parse_geometry_collection
}


def parse_geometry(data) -> Union[GJGeometryObject, None]:
    if data is None:
        return None
    type: str = data["type"].lower()
    if type in typedict:
        return typedict[type](data)
    return None


def parse_feature(data) -> GJFeature:
    feature = GJFeature()
    type: str = data["type"].lower()

    if data["geometry"] is None:
        return None

    if type != "feature":
        raise Exception(f"Excpected GeoJSON type Feature, found type {type}")
    if "geometry" in data:
        feature.geometry = parse_geometry(data["geometry"])
    if "properties" in data:
        feature.meta = data["properties"]
    return feature


def parse_feature_collection(data):
    collection = GJFeatureCollection()
    if "features" in data and data["features"] is not None:
        for feature in data["features"]:
            feature_object = parse_feature(feature)
            if feature_object is not None:
                collection.features.append(feature_object)
    return collection


######################################################################################


def feature_into_collection(feature):
    collection = GJFeatureCollection({})
    collection.features = [feature]
    return collection


def geometry_into_collection(geometry):
    feature = GJFeature({})
    feature.geometry = geometry
    return feature_into_collection(feature)


def parse_any(data):
    if data is None:
        return None

    type: str = data["type"].lower()

    if type == "featurecollection":
        return parse_feature_collection(data)

    try:
        feature = parse_feature(data)
        return feature_into_collection(feature)
    except:
        pass
    try:
        geometry = parse_geometry(data)
        return geometry_into_collection(geometry)
    except:
        return GJFeatureCollection({})


def parse_data(data):
    collection = parse_any(data)
    objects = collection.to_objectlist()
    return objects


def parse(input_file: str):
    contents = read_json(input_file)
    return parse_data(contents)


