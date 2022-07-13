from metacity.utils.filesystem import read_json
from metacity.geometry import Attribute, Model


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
            self.properties = { 'data': None } 


def flatten(data):
    return [item for sublist in data for item in sublist]


def flatten_polygon(polygon):
    return [[item for sublist in ring for item in sublist] for ring in polygon]


def to_model(attr: Attribute):
    model = Model()
    model.add_attribute("POSITION", attr)
    return model


def model_from_point(geometry: Geometry):
    attr = Attribute()
    if geometry.dim == 2:
        attr.push_point2D(geometry.coordinates)
    elif geometry.dim == 3:
        attr.push_point3D(geometry.coordinates)
    return [to_model(attr)]


def model_from_multipoint(geometry: Geometry):
    attr = Attribute()
    if geometry.dim == 2:
        attr.push_point2D(flatten(geometry.coordinates))
    elif geometry.dim == 3:
        attr.push_point3D(flatten(geometry.coordinates))
    return [to_model(attr)]


def model_from_linestring(geometry: Geometry):
    attr = Attribute()
    if geometry.dim == 2:
        attr.push_line2D(flatten(geometry.coordinates))
    elif geometry.dim == 3:
        attr.push_line3D(flatten(geometry.coordinates))
    return [to_model(attr)]


def model_from_multilinestring(geometry: Geometry):
    attr = Attribute()
    dim = geometry.dim
    for line in geometry.coordinates:
        if dim == 2:
            attr.push_line2D(flatten(line))
        elif dim == 3:
            attr.push_line3D(flatten(line))
    return [to_model(attr)]


def model_from_polygon(geometry: Geometry):
    attr = Attribute()
    if geometry.dim == 2:
        attr.push_polygon2D(flatten_polygon(geometry.coordinates))
    elif geometry.dim == 3:
        attr.push_polygon3D(flatten_polygon(geometry.coordinates))
    return [to_model(attr)]


def model_from_multipolygon(geometry: Geometry):
    attr = Attribute()
    dim = geometry.dim
    for polygon in geometry.coordinates:
        if dim == 2:
            attr.push_polygon2D(flatten_polygon(polygon))
        elif dim == 3:
            attr.push_polygon3D(flatten_polygon(polygon))
    return [to_model(attr)]


def model_from_geometrycollection(geometry: Geometry):
    models = []
    for subgeometry in geometry.geometries:
        model_list = typedict[subgeometry.geometry_type](subgeometry)
        models.extend(model_list)
    return models


typedict = {
    "point": model_from_point,
    "multipoint": model_from_multipoint,
    "linestring": model_from_linestring,
    "multilinestring": model_from_multilinestring,
    "polygon": model_from_polygon,
    "multipolygon": model_from_multipolygon,
    "geometrycollection": model_from_geometrycollection
}


def parse_feature(feature: Feature):
    #try:
    model_list = typedict[feature.geometry.geometry_type](feature.geometry)
    #TODO parse metadata
    for model in model_list:
        model.set_metadata(feature.properties)
    return model_list
    #except:
    #    message = f"""
    #    Skipping unsupported or empty features:
    #        type: {feature.geometry.geometry_type}
    #    """
    #    print(message)
    return []


def parse_data(data):
    models = []
    for f in data['features']:
        feature = Feature(f)
        models.extend(parse_feature(feature))
    return models


def parse(input_file: str):
    contents = read_json(input_file)
    return parse_data(contents)


