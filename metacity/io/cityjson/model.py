import itertools
from metacity.datamodel.object import MetacityObject
from metacity.datamodel.primitives.facets import FacetModel
from metacity.datamodel.primitives.points import PointModel
from metacity.datamodel.primitives.lines import LineModel

from metacity.io.cityjson.facets import CJFacetParser


def ensure_iterable(data):
    try:
        _ = iter(data)
        return data
    except TypeError:
        return [ data ]



class CJModelParser:
    def __init__(self, vertices, geometry_object):
        self.vertices = vertices
        self.lod = geometry_object["lod"]
        self.type = geometry_object["type"].lower()
        self.boundries = geometry_object['boundaries']
        self.setup_semantics(geometry_object)


    def setup_semantics(self, geometry_object):
        if 'semantics' in geometry_object:
            self.semantics = geometry_object['semantics']['values'] 
            self.meta = geometry_object['semantics']['surfaces']
        else: 
            self.semantics = None
            self.meta = []
            

    @property
    def is_points(self):
        return self.type == 'multipoint'


    @property
    def is_lines(self):
        return self.type == 'multilinestring'


    @property
    def is_facets(self):
        return self.is_surface or self.is_solid or self.is_multisolid


    @property
    def is_surface(self):
        return self.type == 'multisurface' or self.type == 'compositesurface' 


    @property
    def is_solid(self):
        return self.type == 'solid'


    @property
    def is_multisolid(self):
        return self.type == 'multisolid' or self.type == 'compositesolid'


    def parse(self, object):
        if self.is_points:
            self.load_points(object)
        elif self.is_lines:
            self.load_lines(object)
        elif self.is_facets:
            self.load_facets(object) 
        else:
            raise Exception(f'Unkown CityJSON type: {self.type}')


    def load_points(self, object):
        #TODO load
        pass


    def load_lines(self, object):
        #TODO load
        pass


    def load_facets(self, object: MetacityObject):
        self.model = FacetModel()

        if self.is_surface:   
            self.parse_surface(self.semantics, self.boundries)
        elif self.is_solid:
            self.parse_solid(self.semantics, self.boundries)
        elif self.is_multisolid:
            self.parse_multisolid(self.semantics, self.boundries)

        self.model = self.meta
        object.models.facets.lod[self.lod].join(self.model)


    def parse_multisolid(self, semantics, multisolid):
        for solid, solid_semantic in itertools.zip_longest(multisolid, ensure_iterable(semantics)):
            self.parse_solid(solid_semantic, solid)


    def parse_solid(self, semantics, solid):
        for shell, shell_semantics in itertools.zip_longest(solid, ensure_iterable(semantics)):
            self.parse_surface(shell_semantics, shell)


    def parse_surface(self, semantics, boundries):
        parser = CJFacetParser(self.vertices, boundries, semantics)
        model = parser.parse()
        self.model.join(model)

