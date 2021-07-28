import itertools

from metacity.helpers.iter import ensure_iterable
from metacity.geometry.surfaces import process_model


def get_semantics(geometry_object):
    if 'semantics' in geometry_object:
        return geometry_object['semantics']['values'], geometry_object['semantics']['surfaces']
    else: 
        return None, None


def get_cityjson_geometry_stats(geometry_object):
    lod = geometry_object["lod"]
    gtype = geometry_object["type"].lower()
    return lod, gtype


def load_cj_multisolid(model, vertices, lod, semantics, multisolid):
    for solid, solid_semantic in itertools.zip_longest(multisolid, ensure_iterable(semantics)):
        load_cj_solid(model, vertices, lod, solid_semantic, solid)


def load_cj_solid(model, vertices, lod, semantics, solid):
    for shell, shell_semantics in itertools.zip_longest(solid, ensure_iterable(semantics)):
        load_cj_surface(model, vertices, lod, shell_semantics, shell)


def load_cj_surface(model, vertices, lod, semantics, boundries):
    surface = process_model(vertices, boundries, semantics)
    model.facets.join_model(surface, lod)


def load_cj_facet_semanatic_surfaces(model, lod, semantics):
    if semantics == None:
        return
    model.facets.lod[lod].semantics_meta.extend(semantics)


def load_cj_geometry(model, vertices, geometry_object):
    lod, gtype = get_cityjson_geometry_stats(geometry_object)
    semantic_indices, semantics_surfaces = get_semantics(geometry_object)
    boundries = geometry_object['boundaries']

    if gtype.lower() == 'multipoint':
        pass 
        #self._processPoints(geom['boundaries'], vnp, vertices)
    elif gtype.lower() == 'multilinestring':
        pass
        #for line in geom['boundaries']:
        #    self._processLine(line, vnp, vertices)
    elif gtype.lower() == 'multisurface' or gtype.lower() == 'compositesurface':   
        load_cj_surface(model, vertices, lod, semantic_indices, boundries)
        load_cj_facet_semanatic_surfaces(model, lod, semantics_surfaces)
    elif gtype.lower() == 'solid':
        load_cj_solid(model, vertices, lod, semantic_indices, boundries)
        load_cj_facet_semanatic_surfaces(model, lod, semantics_surfaces)
    elif gtype.lower() == 'multisolid' or gtype.lower() == 'compositesolid':
        load_cj_multisolid(model, vertices, lod, semantic_indices, boundries)
        load_cj_facet_semanatic_surfaces(model, lod, semantics_surfaces)


def clean_cityjson_meta(object):
    return { key: value for key, value in object.items() if key not in ['geometry', 'semantics'] }


def load_cityjson_object(model, object, vertices):
    geometry = object['geometry']
    for geometry_object in geometry:
        load_cj_geometry(model, vertices, geometry_object)
    model.meta = clean_cityjson_meta(object)
    model.consolidate()


