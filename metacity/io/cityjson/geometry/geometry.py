from metacity.io.cityjson.geometry.points import CJPoints
from metacity.io.cityjson.geometry.lines import CJLines
from metacity.io.cityjson.geometry.multisurface import CJMultiSurface
from metacity.io.cityjson.geometry.solid import CJSolid
from metacity.io.cityjson.geometry.multisolid import CJMultiSolid
from metacity.io.cityjson.geometry.geometryinstance import CJGeometryInstance


class CJGeometry:
    def __init__(self, data, vertices, templates):
        self.type = data["type"].lower()

        if self.type == 'geometryinstance':
            self.primitive = CJGeometryInstance(data, vertices, templates)
        elif self.type == 'multipoint':
            self.primitive = CJPoints(data, vertices)
        elif self.type == 'multilinestring':
            self.primitive = CJLines(data, vertices)
        elif self.type == 'multisurface' or self.type == 'compositesurface':
            self.primitive = CJMultiSurface(data, vertices)
        elif self.type == 'solid':
            self.primitive = CJSolid(data, vertices)
        elif self.type == 'multisolid' or self.type == 'compositesolid':
            self.primitive = CJMultiSolid(data, vertices)
        else:
            raise Exception(f'Unknown CityJSON geometry type: {self.type}')

    def export(self):
        return self.primitive.export()
