from tests.data.random import random_semantics, random_vertices
import numpy as np

def random_points(vcount=60, vertex_skip=2):
    vertices = random_vertices(vcount)
    data = {
        "type": "MultiPoint",
        "lod": 1,
        "boundaries": [ i for i in range(0, vcount, vertex_skip) ],
        "semantics": {
            "surfaces" : [
                {
                    "type": "Semantics1",
                }, 
                {
                    "type": "Semantics2",
                },
                {
                    "type": "Semantics3",
                }
            ],
            "values": random_semantics(count=vcount // vertex_skip, srange=3).tolist()
        }
    }

    return vertices, data


def random_lines(vcount=60, segments=[12, 12, 12, 12, 12]):
    vertices = random_vertices(vcount)
    indices = [ i for i in range(vcount) ]

    assert sum(segments) == vcount

    boundaries = []
    prev = 0
    for i in segments:
        boundaries.append(indices[prev:prev + i])
        prev = prev + i 

    data = {
        "type": "MultiLineString",
        "lod": 1,
        "boundaries": boundaries,
        "semantics": {
            "surfaces" : [
                {
                    "type": "Semantics1",
                }, 
                {
                    "type": "Semantics2",
                },
                {
                    "type": "Semantics3",
                }
            ],
            "values": random_semantics(count=len(segments), srange=3).tolist()
        }
    } 

    return vertices, data



def cube_multisurface():
    vertices = np.array([[ 1.0,  0.0,  1.0],
                         [ 0.0,  1.0,  1.0],
                         [-1.0,  0.0,  1.0],
                         [ 0.0, -1.0,  1.0],
                         [ 1.0,  0.0,  0.0],
                         [ 0.0,  1.0,  0.0],
                         [-1.0,  0.0,  0.0],
                         [ 0.0, -1.0,  0.0]])


    boundaries = [[[0,1,2,3]],[[7,4,0,3]],[[4,5,1,0]],[[5,6,2,1]],[[3,2,6,7]],[[6,5,4,7]]]

    data = {
        "type": "MultiSurface",
        "lod": 1,
        "boundaries": boundaries,
        "semantics": {
            "surfaces" : [
                {
                    "type": "Semantics1",
                }, 
                {
                    "type": "Semantics2",
                },
                {
                    "type": "Semantics3",
                }
            ],
            "values": random_semantics(count=len(boundaries), srange=3).tolist()
        }
    } 

    return vertices, data

def cubes_solid():
    vertices = np.array([[ 1.0,  0.0,  1.0],
                         [ 0.0,  1.0,  1.0],
                         [-1.0,  0.0,  1.0],
                         [ 0.0, -1.0,  1.0],
                         [ 1.0,  0.0,  0.0],
                         [ 0.0,  1.0,  0.0],
                         [-1.0,  0.0,  0.0],
                         [ 0.0, -1.0,  0.0]])
    vertices_all = []
    vertices_all.extend(vertices)
    vertices_all.extend(vertices + [2.0, 0.0, 0.0])
    vertices_all = np.array(vertices_all)


    boundaries = [[[0,1,2,3]],[[7,4,0,3]],[[4,5,1,0]],[[5,6,2,1]],[[3,2,6,7]],[[6,5,4,7]]]
    boundaries_all = [boundaries, (np.array(boundaries, dtype=int) + 8).tolist()]

    data = {
        "type": "Solid",
        "lod": 1,
        "boundaries": boundaries_all,
        "semantics": {
            "surfaces" : [
                {
                    "type": "Semantics1",
                }, 
                {
                    "type": "Semantics2",
                },
                {
                    "type": "Semantics3",
                }
            ],
            "values": [random_semantics(count=len(boundaries), srange=3).tolist(),
                       random_semantics(count=len(boundaries), srange=3).tolist()] 
        }
    } 

    return vertices_all, data


def cubes_multisolid():
    vertices = np.array([[ 1.0,  0.0,  1.0],
                         [ 0.0,  1.0,  1.0],
                         [-1.0,  0.0,  1.0],
                         [ 0.0, -1.0,  1.0],
                         [ 1.0,  0.0,  0.0],
                         [ 0.0,  1.0,  0.0],
                         [-1.0,  0.0,  0.0],
                         [ 0.0, -1.0,  0.0]])
    vertices_all = []
    vertices_all.extend(vertices)
    vertices_all.extend(vertices + [2.0, 0.0, 0.0])
    vertices_all = np.array(vertices_all)


    boundaries = [[[0,1,2,3]],[[7,4,0,3]],[[4,5,1,0]],[[5,6,2,1]],[[3,2,6,7]],[[6,5,4,7]]]
    boundaries_all = [[boundaries], [(np.array(boundaries, dtype=int) + 8).tolist()]]

    data = {
        "type": "MultiSolid",
        "lod": 1,
        "boundaries": boundaries_all,
        "semantics": {
            "surfaces" : [
                {
                    "type": "Semantics1",
                }, 
                {
                    "type": "Semantics2",
                },
                {
                    "type": "Semantics3",
                }
            ],
            "values": [[random_semantics(count=len(boundaries), srange=3).tolist()],
                       [random_semantics(count=len(boundaries), srange=3).tolist()]] 
        }
    } 

    return vertices_all, data

