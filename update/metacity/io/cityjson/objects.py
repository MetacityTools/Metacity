from metacity.datamodel.object import MetacityObject
from metacity.io.cityjson.model import CJModelParser



class CJObjectParser:
    def __init__(self, vertices, oid, object_data):
        self.vertices = vertices
        self.oid = oid
        self.object_data = object_data


    def parse(self, obj: MetacityObject): 
        geometry = self.object_data['geometry']


        for geometry_object in geometry:
            parser = CJModelParser(self.vertices, geometry_object)
            parser.parse(obj)

        
        obj.meta = self.clean_meta(self.object_data)
        obj.oid = self.oid


    def clean_meta(self, data):
        return { key: value for key, value in data.items() if key not in ['geometry', 'semantics'] }