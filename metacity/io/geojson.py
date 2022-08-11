from numpy import number
from metacity.utils.filesystem import read_json
from metacity.geometry import Attribute, Model, Progress
from typing import List, Union
from pyproj import Proj, Transformer


__all__ = ["parse", "parse_data"]



class Projector:
    def __init__(self, from_crs: str = None, to_crs: str = None):
        self.from_crs = from_crs
        self.to_crs = to_crs
        self.transform = None

        if from_crs is None or to_crs is None:
            return

        proj_from = Proj(from_crs, preserve_units=False)
        proj_to = Proj(to_crs, preserve_units=False)
        self.transform = Transformer.from_proj(proj_from, proj_to)

    def project(self, coordinates: List[List[float]]):
        if self.transform is None:
            return coordinates
        return [ p for p in self.transform.itransform(coordinates) ]


class Geometry:
    def __init__(self, data):
        self.data = data
        self.transform = None

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

    def set_projection(self, projector: Projector):
        if projector is None:
            return
        self.transform = projector.transform

    def project(self, coordinates: List[List[float]]):
        if self.transform is None:
            return coordinates
        return [ p for p in self.transform.itransform(coordinates) ]

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


def parse_point(g: Geometry, attr: Attribute, dim: int, vertices: List[List[float]]):
    vertices = g.project(vertices)
    vertices = flatten(vertices)
    if dim == 2:
        attr.push_point2D(vertices)
    elif dim == 3:
        attr.push_point3D(vertices)


def parse_line(g: Geometry, attr: Attribute, dim: int, line: List[List[float]]):
    l = g.project(line)
    l = flatten(line)
    if dim == 2:
        attr.push_line2D(l)
    elif dim == 3:
        attr.push_line3D(l)


def parse_polygon(g: Geometry, attr: Attribute, dim: int, polygon: List[List[List[float]]]):
    polygon = [ g.project(p) for p in polygon ]
    p = flatten_polygon(polygon)
    if dim == 2:
        attr.push_polygon2D(p)
    elif dim == 3:
        attr.push_polygon3D(p)


###############################################################################


def attr_from_point(geometry: Geometry):
    attr = Attribute()
    vertices = [geometry.coordinates]
    parse_point(geometry, attr, geometry.dim, vertices)
    return [attr]


def attr_from_multipoint(geometry: Geometry):
    attr = Attribute()
    vertices = geometry.coordinates
    parse_point(geometry, attr, geometry.dim, vertices)
    return [attr]


def attr_from_linestring(geometry: Geometry):
    attr = Attribute()
    vertices = geometry.coordinates
    parse_line(geometry, attr, geometry.dim, vertices)
    return [attr]


def attr_from_multilinestring(geometry: Geometry):
    attr = Attribute()
    dim = geometry.dim
    for line in geometry.coordinates:
        parse_line(geometry, attr, dim, line)
    return [attr]


def attr_from_polygon(geometry: Geometry):
    attr = Attribute()
    vertices = geometry.coordinates
    parse_polygon(geometry, attr, geometry.dim, vertices)
    return [attr]


def attr_from_multipolygon(geometry: Geometry):
    attr = Attribute()
    dim = geometry.dim
    for polygon in geometry.coordinates:
        parse_polygon(geometry, attr, dim, polygon)
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


def parse_geometry(feature: Feature, projector: Projector):
    feature.geometry.set_projection(projector)
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


def parse_feature(feature: Feature, projector: Projector, progress: Progress):
    attr_list = parse_geometry(feature, projector)
    models = parse_models(feature, attr_list, progress)
    return models


def parse_data(data, from_crs: str, to_crs: str, progress: Progress = None):
    models = []
    projector = Projector(from_crs, to_crs)
    for f in data['features']:
        feature = Feature(f)
        models.extend(parse_feature(feature, projector, progress))
    return models


def parse(input_file: str, from_crs: str = None, to_crs: str = None, progress: Progress = None):
    contents = read_json(input_file)
    return parse_data(contents, from_crs, to_crs, progress)


