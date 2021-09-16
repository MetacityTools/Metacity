import json

from metacity.datamodel.layer.layer import MetacityLayer
from metacity.io.geojson.feature import (GJFeature, GJFeatureCollection,
                                         parse_feature)
from metacity.io.geojson.geometry.collection import parse_geometry


def feature_into_collection(feature):
    collection = GJFeatureCollection({})
    collection.parsed = [feature]
    return collection


def geometry_into_collection(geometry):
    feature = GJFeature({})
    feature.model = geometry      
    return feature_into_collection(feature)
   

def parse_any(data):
    if data is None:
        return None
    type: str = data["type"].lower()
    if type == "featurecollection":
        return GJFeatureCollection(data)
    
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


class GJParser:
    def __init__(self, data):
        self.data = data
        self.collection = parse_any(self.data)

    def set_layer_shift(self, layer: MetacityLayer):
        vs = self.collection.vertices
        layer.config.apply(vs)
    
    def export(self, layer: MetacityLayer):
        if self.collection is not None:
            self.collection.export(layer, layer.config.shift)
            

def parse(layer: MetacityLayer, input_file: str):
    with open(input_file, 'r') as file:
        contents = json.load(file)

    parser = GJParser(contents)
    parser.set_layer_shift(layer)
    parser.export(layer)
