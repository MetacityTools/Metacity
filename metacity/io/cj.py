import itertools
import json
from typing import Dict

import numpy as np
from metacity.geometry.surfaces import process_model
from metacity.helpers.iter import ensure_iterable
from metacity.models.object import MetacityObject
from metacity.project import MetacityLayer
from tqdm import tqdm


def get_cj_semantics(geometry_object):
    if 'semantics' in geometry_object:
        return geometry_object['semantics']['values'], geometry_object['semantics']['surfaces']
    else: 
        return None, None


def get_cj_geometry_stats(geometry_object):
    lod = geometry_object["lod"]
    gtype = geometry_object["type"].lower()
    return lod, gtype


def load_cj_multisolid(object, vertices, lod, semantics, multisolid):
    for solid, solid_semantic in itertools.zip_longest(multisolid, ensure_iterable(semantics)):
        load_cj_solid(object, vertices, lod, solid_semantic, solid)


def load_cj_solid(object, vertices, lod, semantics, solid):
    for shell, shell_semantics in itertools.zip_longest(solid, ensure_iterable(semantics)):
        load_cj_surface(object, vertices, lod, shell_semantics, shell)


def load_cj_surface(object, vertices, lod, semantics, boundries):
    surface = process_model(vertices, boundries, semantics)
    object.facets.join_model(surface, lod)


def load_cj_facet_semanatic_surfaces(object, lod, semantics):
    if semantics == None:
        return
    object.facets.lod[lod].semantics_meta.extend(semantics)


def load_cj_geometry(object, vertices, geometry_object):
    lod, gtype = get_cj_geometry_stats(geometry_object)
    semantic_indices, semantics_surfaces = get_cj_semantics(geometry_object)
    boundries = geometry_object['boundaries']

    if gtype.lower() == 'multipoint':
        pass 
        #self._processPoints(geom['boundaries'], vnp, vertices)
    elif gtype.lower() == 'multilinestring':
        pass
        #for line in geom['boundaries']:
        #    self._processLine(line, vnp, vertices)
    elif gtype.lower() == 'multisurface' or gtype.lower() == 'compositesurface':   
        load_cj_surface(object, vertices, lod, semantic_indices, boundries)
        load_cj_facet_semanatic_surfaces(object, lod, semantics_surfaces)
    elif gtype.lower() == 'solid':
        load_cj_solid(object, vertices, lod, semantic_indices, boundries)
        load_cj_facet_semanatic_surfaces(object, lod, semantics_surfaces)
    elif gtype.lower() == 'multisolid' or gtype.lower() == 'compositesolid':
        load_cj_multisolid(object, vertices, lod, semantic_indices, boundries)
        load_cj_facet_semanatic_surfaces(object, lod, semantics_surfaces)


def clean_cj_meta(object):
    return { key: value for key, value in object.items() if key not in ['geometry', 'semantics'] }


def load_cj_object(object, oid: str, cjobject: Dict, vertices):
    geometry = cjobject['geometry']
    for geometry_object in geometry:
        load_cj_geometry(object, vertices, geometry_object)
    object.meta = clean_cj_meta(cjobject)
    object.oid = oid
    object.consolidate()


def parse_cj_file(input_file):
    with open(input_file, "r") as file:
        contents = json.load(file)

    objects: Dict[str, Dict] = contents["CityObjects"] 
    vertices = np.array(contents["vertices"])
    return objects, vertices


def is_empty(objects, vertices):
    return len(vertices) == 0 or len(objects) == 0


def load_cj_file(layer: MetacityLayer, input_file: str):
    objects, vertices = parse_cj_file(input_file)

    if is_empty(objects, vertices):
        return

    layer.update_config(vertices)
    
    for oid, object in tqdm(objects.items()):
        mobject = MetacityObject()
        load_cj_object(mobject, oid, object, vertices)
        mobject.export_base(layer.dirtree)

