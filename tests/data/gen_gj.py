import numpy as np
import json


def point(dim=2):
    verts = gen_point(dim)
    return get_point_gj(verts, dim)


def get_point_gj(verts, dims):
    return {
        "type" : "Feature",
        "geometry" : {
            "type" : "Point",
            "coordinates" : verts.tolist()
        },
        "properties" : {
            "dimensions": dims
        }
    }


def gen_point(dim):
    verts = np.random.rand(dim).astype(np.float32) * 100
    return verts


def multipoint(dim=2):
    verts = gen_points(dim)
    return get_multipoint_gj(verts, dim)


def get_multipoint_gj(verts, dims):
    return {
        "type" : "Feature",
        "geometry" : {
            "type" : "MultiPoint",
            "coordinates" : verts.tolist()
        },
        "properties" : {
            "dimensions": dims
        }
    }


def gen_points(dim, count=20):
    verts = np.random.rand(count, dim).astype(np.float32) * 100
    return verts


def linestring(dim=2):
    verts = gen_points(dim)
    return get_multipoint_gj(verts, dim)


def get_linestring_gj(verts, dims):
    return {
        "type" : "Feature",
        "geometry" : {
            "type" : "LineString",
            "coordinates" : verts.tolist()
        },
        "properties" : {
            "dimensions": dims
        }
    }


def multilinestring(dim=2):
    verts = np.array([gen_points(dim) for i in range(5)])
    return get_multilinestring_gj(verts, dim)


def get_multilinestring_gj(verts, dims):
    return {
        "type" : "Feature",
        "geometry" : {
            "type" : "MultiLineString",
            "coordinates" : verts.tolist()
        },
        "properties" : {
            "dimensions": dims
        }
    }


def polygon(dim=2):
    verts = gen_polygon(dim)
    return get_polygon_gj(verts, dim)


def gen_polygon(dim):
    verts = gen_points(dim, count=6)
    # flatten
    if dim == 3:
        verts[:, 2] = 0
    verts = np.append(verts, [verts[0]], axis=0)
    # TODO should be ordered according to right hand rule
    return verts


def get_polygon_gj(verts, dims):
    return {
        "type" : "Feature",
        "geometry" : {
            "type" : "Polygon",
            "coordinates" : [ verts.tolist() ]
        },
        "properties" : {
            "dimensions": dims
        }
    }


def multipolygon(dim=2):
    verts = np.array([gen_polygon(dim) for i in range(5)])
    return get_multipolygon_gj(verts, dim)


def get_multipolygon_gj(verts, dims):
    return {
        "type" : "Feature",
        "geometry" : {
            "type" : "MultiPolygon",
            "coordinates" : [ verts.tolist() ]
        },
        "properties" : {
            "dimensions": dims
        }
    }


def geometrycollection(dim=2):
    geometries = [point(dim), multipoint(dim), linestring(dim), multilinestring(dim), polygon(dim), multipolygon(dim)]
    for g in geometries:
        del g["type"]
    return get_geometrycollection_gj(geometries, dim)


def get_geometrycollection_gj(geometries, dims):
    return {
        "type" : "GeometryCollection",
        "geometries" : geometries,
        "properties" : {
            "dimensions": dims
        }
    }


def gen_features(dim):
    return point(dim), multipoint(dim), linestring(dim), multilinestring(dim), polygon(dim), multipolygon(dim), geometrycollection(dim)


geojson = {
    "type": "FeatureCollection",
       "features": [
           *gen_features(2),
           *gen_features(3)
       ]
}

print(geojson)

with open("gjdata.json", 'w') as file:
    json.dump(geojson, file, indent=4)