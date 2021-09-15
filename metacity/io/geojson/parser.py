from metacity.datamodel.primitives.facets import FacetModel
from metacity.utils.surface import Surface
from metacity.datamodel.primitives.lines import LineModel
from metacity.datamodel.primitives.points import PointModel
import numpy as np
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.filesystem import layer as fs
import geojson
from tqdm import tqdm
import itertools
from earcut import earcut as ec


class GJObject:
    def __init__(self, data):
        self.data = data


class GJModelObject(GJObject):
    def __init__(self, data):
        super().__init__(data)

    @property
    def formated_coords(self):
        data = np.array(self.data["coordinates"], dtype=np.float32)
        if data.shape[-1] == 2:
            pads = [(0, 0)] * (data.ndim - 1)
            pads.append((0, 1))
            data = np.pad(data, pads)
        if data.shape[-1] != 3:
            raise Exception(f"Coordinate data have an unexpected shape: {data.shape}")
        return data

    def empty_semantics(self, nvert):
        return np.array([-1] * nvert, dtype=np.int32)


class GJPoint(GJModelObject):
    def __init__(self, data):
        super().__init__(data)
        model = self.prep_model()
        self.parsed = [model]

    def prep_model(self):
        model = PointModel()
        model.buffers.vertices.set(self.formated_coords.flatten())
        nvert = model.buffers.vertices.shape[0] // 3
        model.buffers.semantics.set(self.empty_semantics(nvert))
        return model


class GJMultiPoint(GJPoint):
    def __init__(self, data):
        super().__init__(data)
        # that is all


class GJLine(GJModelObject):
    def __init__(self, data):
        super().__init__(data)
        model = self.prep_model()
        self.parsed = [model]

    def prep_model(self):
        model = LineModel()
        vs = self.prep_coords()
        model.buffers.vertices.set(vs.flatten())
        nvert = model.buffers.vertices.shape[0] // 3
        model.buffers.semantics.set(self.empty_semantics(nvert))
        return model

    def prep_coords(self):
        return np.repeat(self.formated_coords, 2, axis=0)[1:-1]


class GJMultiLine(GJLine):
    def __init__(self, data):
        super().__init__(data)

    def prep_coords(self):
        verts = []
        for linestring in self.formated_coords:
            verts.append(np.repeat(linestring, 2, axis=0)[1:-1])
        return np.concatenate(verts, dtype=np.float32)


class GJPolygon(GJModelObject):
    def __init__(self, data):
        super().__init__(data)

    def triangulate(self, coords):
        data = ec.flatten(coords)
        vs = np.array(data["vertices"])
        normal, normal_exists = ec.normal(vs)
        if not normal_exists:
            return Surface()
        ti = ec.earcut(vs, data["holes"], 3)
        vs.reshape((vs.shape[0] // 3, 3))
        v = np.array(vs[ti], dtype=np.float32)
        tri_count = len(ti)    
        n = np.repeat([normal], tri_count, axis=0).astype(np.float32)    
        s = np.repeat([-1], tri_count, axis=0).astype(np.int32)   
        return Surface(v, n, s)

    def prep_model(self):
        model = FacetModel()
        surface = self.parse_coordiantes()
        model.buffers.vertices.set(np.array(surface.v, dtype=np.float32))
        model.buffers.vertices.set(np.array(surface.n, dtype=np.float32))
        model.buffers.semantics.set(np.array(surface.s, dtype=np.int32))
        return model

    def parse_coordiantes(self):
        return self.triangulate(self.data["coordinates"])


class GJMultiPolygon(GJPolygon):
    def __init__(self, data):
        super().__init__(data)

    def parse_coordiantes(self):
        s = Surface()
        for surface in self.data["coordinates"]:
            s.join(self.triangulate(surface))
        return s


class GJFeature(GJObject):
    def __init__(self, data):
        super().__init__(data)
        self.models = [parse_object(self.data["geometry"])]
        if "properties" in self.data:
            self.meta = data["properties"]
        else: 
            self.meta = {}

    def __repr__(self):
        return f"<Feature: {[m for m in self.models]}>"


class GJGeometryCollection(GJObject):
    def __init__(self, data):
        super().__init__(data)
        self.parsed = [parse_object(obj) for obj in self.data["geometries"]]
        self.meta = {}

    def __repr__(self):
        return f"<GeometryCollection: {[f for f in self.parsed]}>"


class GJFeatureCollection(GJObject):
    def __init__(self, data):
        super().__init__(data)
        self.parsed = [parse_object(obj) for obj in self.data["features"]]
        self.meta = {}

    def __repr__(self):
        return f"<FeatureColection: {[f for f in self.parsed]}>"


type_dict = {
    "FeatureCollection": GJFeatureCollection,
    "GeometryCollection": GJGeometryCollection,
    "Feature": GJFeature,
    "Point": GJPoint,
    "MultiPoint": GJMultiPoint,
    "LineString": GJLine,
    "MultiLineString": GJMultiLine,
    "Polygon": GJPolygon,
    "MultiPolygon": GJMultiPolygon 
}


def parse_object(data):
    type = data["type"]
    if type not in type_dict:
        raise Exception(f"Unexpected type encountered while parsing GeoJSON file: {type}")
    return type_dict[type](data)
    

class GJParser:
    def __init__(self, data):
        self.data = data

    def adjust_data(self, layer: MetacityLayer):
        pass

    def parse(self):
        self.parsed = parse_object(self.data)
            



def parse(layer: MetacityLayer, input_file: str):
    with open(input_file, 'r') as file:
        contents = geojson.load(file)

    parser = GJParser(contents)
    parser.parse()
    pprint(parser.parsed)