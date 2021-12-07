from metacity.filesystem.base import read_json
from typing import List, Union
from metacity.datamodel.object import Object
from abc import ABC, abstractmethod
import metacity.geometry as p


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
    def to_models(self):
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

    def to_models(self):
        model = p.MultiPoint()
        if self.dim == 2:
            model.push_p2(self.coordinates)
        elif self.dim == 3:
            model.push_p3(self.coordinates)
        return [model]


class GJMultiPoint(GJPoint):
    def __init__(self):
        super().__init__()

    def to_models(self):
        model = p.MultiPoint()
        if self.dim == 2:
            model.push_p2(flatten(self.coordinates))
        elif self.dim == 3:
            model.push_p3(flatten(self.coordinates))
        return [model]


class GJLine(GJGeometryObject):
    def __init__(self):
        super().__init__()

    def parse(self, data):
        self.set_coordinates(data)

    def to_models(self):
        model = p.MultiLine()
        if self.dim == 2:
            model.push_l2(flatten(self.coordinates))
        elif self.dim == 3:
            model.push_l3(flatten(self.coordinates))
        return [model]


class GJMultiLine(GJLine):
    def __init__(self):
        super().__init__()

    def to_models(self):
        model = p.MultiLine()
        dim = self.dim
        for line in self.coordinates:
            if dim == 2:
                model.push_l2(flatten(line))
            elif dim == 3:
                model.push_l3(flatten(line))
        return [model]


class GJPolygon(GJGeometryObject):
    def __init__(self):
        super().__init__()

    def parse(self, data):
        self.set_coordinates(data)

    def to_models(self):
        model = p.MultiPolygon()
        dim = self.dim
        if dim == 2:
            model.push_p2(flatten_polygon(self.coordinates))
        elif dim == 3:
            model.push_p3(flatten_polygon(self.coordinates))
        return [model]


class GJMultiPolygon(GJPolygon):
    def __init__(self):
        super().__init__()

    def to_models(self):
        model = p.MultiPolygon()
        dim = self.dim
        for polygon in self.coordinates:
            if dim == 2:
                model.push_p2(flatten_polygon(polygon))
            elif dim == 3:
                model.push_p3(flatten_polygon(polygon))
        return [model]


class GJGeometryCollection(GJGeometryObject):
    def __init__(self):
        super().__init__()
        self.geometries: List[GJGeometryObject] = []

    def to_models(self):
        return [model for geometry in self.geometries for model in geometry.to_models()]


class GJFeature:
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.geometry: GJGeometryObject = None

    def to_object(self):
        o = Object()
        o.models = self.geometry.to_models()
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
    model = GJPoint()
    model.parse(data)
    return model


def parse_multipoint(data):
    model = GJMultiPoint()
    model.parse(data)
    return model


def parse_line(data):
    model = GJLine()
    model.parse(data)
    return model


def parse_multiline(data):
    model = GJMultiLine()
    model.parse(data)
    return model


def parse_polygon(data):
    model = GJPolygon()
    model.parse(data)
    return model


def parse_multipolygon(data):
    model = GJMultiPolygon()
    model.parse(data)
    return model


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


