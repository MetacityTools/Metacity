from metacity.utils.filesystem import read_json
from metacity.geometry import Attribute, Model, Progress
from typing import List, Union


__all__ = ["parse", "parse_data"]


class Geometry:
    def __init__(self, data):
        self.data = data

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

    @property
    def coordinates(self):
        return self.data['coordinates']

    @property
    def geometry_type(self):
        return self.data['type'].lower()

    @property
    def geometries(self):
        return [Geometry(g) for g in self.data['geometries']]


class Feature:
    def __init__(self, data):
        self.geometry = Geometry(data['geometry'])
        if 'properties' in data:
            self.properties = data['properties']
        else:
            self.properties = {} 


def flatten(data):
    return [item for sublist in data for item in sublist]


def flatten_polygon(polygon):
    return [[item for sublist in ring for item in sublist] for ring in polygon]


def to_model(attr: Attribute):
    model = Model()
    model.add_attribute("POSITION", attr)
    return model


###############################################################################


def parse_point(attr: Attribute, dim: int, vertices: List[List[float]]):
    vertices = flatten(vertices)
    if dim == 2:
        attr.push_point2D(vertices)
    elif dim == 3:
        attr.push_point3D(vertices)


def parse_line(attr: Attribute, dim: int, line: List[List[float]]):
    l = flatten(line)
    if dim == 2:
        attr.push_line2D(l)
    elif dim == 3:
        attr.push_line3D(l)


def parse_polygon(attr: Attribute, dim: int, polygon: List[List[List[float]]]):
    p = flatten_polygon(polygon)
    if dim == 2:
        attr.push_polygon2D(p)
    elif dim == 3:
        attr.push_polygon3D(p)


###############################################################################


def attr_from_point(geometry: Geometry):
    attr = Attribute()
    vertices = [geometry.coordinates]
    parse_point(attr, geometry.dim, vertices)
    return [attr]


def attr_from_multipoint(geometry: Geometry):
    attr = Attribute()
    vertices = geometry.coordinates
    parse_point(attr, geometry.dim, vertices)
    return [attr]


def attr_from_linestring(geometry: Geometry):
    attr = Attribute()
    vertices = geometry.coordinates
    parse_line(attr, geometry.dim, vertices)
    return [attr]


def attr_from_multilinestring(geometry: Geometry):
    attr = Attribute()
    dim = geometry.dim
    for line in geometry.coordinates:
        parse_line(attr, dim, line)
    return [attr]


def attr_from_polygon(geometry: Geometry):
    attr = Attribute()
    vertices = geometry.coordinates
    parse_polygon(attr, geometry.dim, vertices)
    return [attr]


def attr_from_multipolygon(geometry: Geometry):
    attr = Attribute()
    dim = geometry.dim
    for polygon in geometry.coordinates:
        parse_polygon(attr, dim, polygon)
    return [attr]


def attr_from_geometrycollection(geometry: Geometry):
    attrs = []
    for subgeometry in geometry.geometries:
        if subgeometry.geometry_type not in typedict:
            raise Exception(f"Unknown geometry type {subgeometry.geometry_type}")
        attr_list = typedict[subgeometry.geometry_type](subgeometry)
        attrs.extend(attr_list)
    return attrs


typedict = {
    "point": attr_from_point,
    "multipoint": attr_from_multipoint,
    "linestring": attr_from_linestring,
    "multilinestring": attr_from_multilinestring,
    "polygon": attr_from_polygon,
    "multipolygon": attr_from_multipolygon,
    "geometrycollection": attr_from_geometrycollection
}


def parse_geometry(feature: Feature):
    if feature.geometry.geometry_type not in typedict:
        raise Exception(f"Unknown geometry type {feature.geometry.geometry_type}")
    attr_list = typedict[feature.geometry.geometry_type](feature.geometry)
    return attr_list


def parse_models(feature: Feature, attr_list: List[Attribute], progress: Union[Progress, None]):
    models = []
    for attr in attr_list:
        if progress is not None:
            progress.update()
        model = to_model(attr)
        model.set_metadata(feature.properties)
        models.append(model)
    return models


def parse_feature(feature: Feature, progress: Progress):
    attr_list = parse_geometry(feature)
    models = parse_models(feature, attr_list, progress)
    return models


def parse_data(data, progress: Progress = None):
    models = []
    for f in data['features']:
        feature = Feature(f)
        models.extend(parse_feature(feature, progress))
    return models


def parse(input_file: str, progress: Progress = None):
    contents = read_json(input_file)
    return parse_data(contents, progress)


