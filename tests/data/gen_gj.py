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
    return get_linestring_gj(verts, dim)


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
    verts = [gen_points(dim, count=(i + 1) * 10).tolist() for i in range(5)]
    return get_multilinestring_gj(verts, dim)


def get_multilinestring_gj(verts, dims):
    return {
        "type" : "Feature",
        "geometry" : {
            "type" : "MultiLineString",
            "coordinates" : verts
        },
        "properties" : {
            "dimensions": dims
        }
    }


def polygon(dim=2):
    verts = gen_polygon(dim)
    return get_polygon_gj(verts, dim)


def gen_polygon(dim, count=6):
    verts = gen_points(dim, count=count)
    # flatten
    if dim == 3:
        verts[:, 2] = 0
    
    verts = anti_clock_sort(verts)
    return verts


def anti_clock_sort(verts):
    center = np.sum(verts, axis=0) / len(verts)
    vec2 = (verts - center)[:, :2]
    cplx = vec2[:, 0] + vec2[:, 1] * 1j
    angles = np.angle(cplx)
    avert = np.array([v for _, v in sorted(zip(angles, verts), key=lambda pair: pair[0])])
    verts = np.append(avert, [avert[0]], axis=0)
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
    verts = [[gen_polygon(dim, count=(i + 1) * 3).tolist() ] for i in range(5)]
    return get_multipolygon_gj(verts, dim)


def get_multipolygon_gj(verts, dims):
    return {
        "type" : "Feature",
        "geometry" : {
            "type" : "MultiPolygon",
            "coordinates" : verts
        },
        "properties" : {
            "dimensions": dims
        }
    }


def geometrycollection(dim=2):
    geometries = [ g["geometry"] for g in [point(dim), multipoint(dim), linestring(dim), multilinestring(dim), polygon(dim), multipolygon(dim)] ]
    return get_geometrycollection_gj(geometries, dim)


def get_geometrycollection_gj(geometries, dims):
    return {
        "type" : "Feature",
        "geometry" : {
            "type": "GeometryCollection",
            "geometries": geometries
        },
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