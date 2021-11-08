#from metacity.datamodel.project import Project
#from metacity.datamodel.layer import Layer, LayerOverlay, LayerMetaIterator
#from metacity.datamodel.grid import Grid, TileCache
#from metacity.datamodel.object import Object
#from metacity.datamodel.set import DataSet, ModelSet, MetaSet, ObjectSet, TileSet, Tile
#from metacity.datamodel.styles import ProjectStyleSet
#from metacity.styles.styles import STYLEGRAMMAR, Style, TreeToStyle, LayerStyler
#from metacity.geometry import Primitive, MultiPoint, MultiLine, MultiPolygon, SimpleMultiPoint, SimpleMultiLine, SimpleMultiPolygon
#from metacity.io.geojson.parser import GJGeometryObject, GJPoint, GJMultiLine, GJPolygon, GJFeature, GJFeatureCollection, GJGeometryCollection, parse
#from metacity.io.shapefile.parser import parse
#from metacity.io.cityjson import *
#from metacity.utils.bbox import bboxes_bbox, vertices_bbox, empty_bbox
#from metacity.utils.persistable import Persistable
#from metacity.utils.encoding import *

"""
Metacity is a library for creating and manipulating city objects. It supports the following formats: GeoJSON, Shapefile, and CityJSON. City objects are represented as an array of objects, each of which has a set of properties. The properties include a geometry, and a set of metadata. The appearance of the city objects is defined by a set of styles. The styles are specified with a custom language. The library is designed to be extensible, so that new types of objects and styles can be added.
"""