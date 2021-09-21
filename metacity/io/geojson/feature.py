from typing import List
from metacity.io.geojson.geometry.collection import parse_geometry
from metacity.io.geojson.geometry.base import GJObject
from metacity.datamodel.object import MetacityObject
from metacity.datamodel.layer.layer import MetacityLayer
import numpy as np


class GJFeature(GJObject):
    def __init__(self, data):
        super().__init__(data)
        self.meta = {}
        self.model = None
        if "geometry" in self.data: 
            self.model = parse_geometry(self.data["geometry"])
        if "properties" in self.data:
            self.meta = data["properties"] 

    def __repr__(self):
        return f"<Feature: {[m for m in self.models]}>"

    @property
    def vertices(self):
        if self.model is None:
            return np.array([])
        return self.model.vertices

    def to_metaobject(self, layer: MetacityLayer, shift):
        obj = MetacityObject()
        if 'id' in self.meta:
            obj.oid = self.meta['id']
        else:
            obj.oid = layer.generate_oid()
        
        if self.model is not None:
            for m in self.model.to_primitives(shift):
                obj.models.models.append(m)
        obj.meta = self.meta
        return obj


def parse_feature(data) -> GJFeature:
    type: str = data["type"].lower()
    if type != "feature":
        raise Exception(f"Excpected GeoJSON type Feature, found type {type}")
    return GJFeature(data)


class GJFeatureCollection(GJObject):
    def __init__(self, data):
        super().__init__(data)
        self.features: List[GJFeature] = []
        self.parse_features()

    def __repr__(self):
        return f"<FeatureColection: {[f for f in self.features]}>"

    @property
    def vertices(self):
        if len(self.features) == 0:
            return np.array([])
        vertices = [feature.vertices for feature in self.features]
        return np.concatenate(vertices, axis=0)

    def parse_features(self):
        if "features" in self.data and self.data["features"] is not None: 
            for feature in self.data["features"]:
                ftr = parse_feature(feature)
                if ftr != None:
                    self.features.append(ftr)

    def export(self, layer: MetacityLayer, shift):
        geometry_path = layer.geometry_path
        meta_path = layer.meta_path
        for feature in self.features:
            obj = feature.to_metaobject(layer, shift)
            obj.export(geometry_path, meta_path)            
