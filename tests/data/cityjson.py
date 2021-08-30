

from tests.data.random import random_semantics, random_vertices


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