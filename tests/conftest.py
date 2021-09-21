from metacity.grid.build import generate_layout
import os

import metacity.utils.bbox as bbox
import numpy as np
import pytest
from metacity.datamodel.grid.grid import RegularGrid
from metacity.datamodel.layer.layer import MetacityLayer

from metacity.datamodel.primitives import facets
from metacity.datamodel.primitives import lines
from metacity.datamodel.primitives import points


######################################
# GEOMETRY
######################################


def gen_random_vertices(count=30):
    coordinates = np.random.rand(count, 3).astype(np.float32) * 1000
    return coordinates


@pytest.fixture(scope="function")
def random_vertices():
    yield gen_random_vertices()



def gen_random_vertices_normals(count=30):
    vertices = gen_random_vertices(count)
    vert = vertices.reshape((vertices.shape[0] // 3, 3, 3))
    normals = []
    for a, b, c in vert:
        normals.extend(np.cross(b - a, c - a))

    normals = np.array(normals, dtype=np.float32)
    normals = np.repeat(normals, 3, axis=0)
    return vertices, normals


@pytest.fixture(scope="function")
def random_vertices_normals(count=30):
    yield gen_random_vertices_normals()


def gen_random_semantics(count=30, srange=10):
    indices = np.random.randint(0, srange, size=(count,), dtype=np.int32)
    return indices


@pytest.fixture(scope="function")
def random_semantics(count=30, srange=10):
    yield gen_random_semantics()


def gen_random_semantic_meta():
    return [{'attribute': 'test value'}]


@pytest.fixture(scope="function")
def random_semantic_meta():
    yield gen_random_semantic_meta()


def gen_random_bbox():
    return bbox.vertices_bbox(gen_random_vertices())


@pytest.fixture(scope="function")
def random_bbox():
    yield gen_random_bbox()


def gen_random_bboxes():
    return [bbox.vertices_bbox(gen_random_vertices()) for i in range(30)]


@pytest.fixture(scope="function")
def random_bboxes():
    yield gen_random_bboxes()


######################################
# CITYJSON
######################################


def gen_random_points(vcount=60, vertex_skip=2):
    vertices = gen_random_vertices(vcount)
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
            "values": gen_random_semantics(count=vcount // vertex_skip, srange=3).tolist()
        }
    }

    return vertices, data


@pytest.fixture(scope="function")
def random_points():
    yield gen_random_points()


def gen_random_lines(vcount=60, segments=[12, 12, 12, 12, 12]):
    vertices = gen_random_vertices(vcount)
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
            "values": gen_random_semantics(count=len(segments), srange=3).tolist()
        }
    } 

    return vertices, data


@pytest.fixture(scope="function")
def random_lines():
    yield gen_random_lines()


def gen_cube_multisurface():
    vertices = np.array([[ 1.0,  0.0,  1.0],
                         [ 0.0,  1.0,  1.0],
                         [-1.0,  0.0,  1.0],
                         [ 0.0, -1.0,  1.0],
                         [ 1.0,  0.0,  0.0],
                         [ 0.0,  1.0,  0.0],
                         [-1.0,  0.0,  0.0],
                         [ 0.0, -1.0,  0.0]])


    boundaries = [[[0, 1,2,3]],[[7,4,0,3]],[[4,5,1,0]],[[5,6,2,1]],[[3,2,6,7]],[[6,5,4,7]]]

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
            "values": gen_random_semantics(count=len(boundaries), srange=3).tolist()
        }
    } 

    return vertices, data


@pytest.fixture(scope="function")
def cube_multisurface():
    yield gen_cube_multisurface()


def gen_cubes_solid():
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
            "values": [gen_random_semantics(count=len(boundaries), srange=3).tolist(),
                       gen_random_semantics(count=len(boundaries), srange=3).tolist()] 
        }
    } 

    return vertices_all, data


@pytest.fixture(scope="function")
def cubes_solid():
    yield gen_cubes_solid()


def gen_cubes_multisolid():
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
            "values": [[gen_random_semantics(count=len(boundaries), srange=3).tolist()],
                       [gen_random_semantics(count=len(boundaries), srange=3).tolist()]] 
        }
    } 

    return vertices_all, data


@pytest.fixture(scope="function")
def cubes_multisolid():
    yield gen_cubes_multisolid()


######################################
# DATASETS
######################################


def data_dir():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    return package_dir


class DatasetStats:
    def __init__(self):
        self.obj_count = 0
        self.gtypes = {}


@pytest.fixture(scope='function')
def railway_dataset():
    dataset_path = os.path.join(data_dir(), 'data', 'dataset.json')
    yield dataset_path


@pytest.fixture(scope='function')
def geojson_dataset():
    dataset_path = os.path.join(data_dir(), 'data', 'gjdata.json')
    yield dataset_path


@pytest.fixture(scope='function')
def railway_dataset_stats():
    stats = DatasetStats()
    stats.obj_count = 121
    stats.gtypes = {
        'multisurface': 104,
        'geometryinstance': 15,
        'compositesurface': 1,
    }

    yield stats


@pytest.fixture(scope="function")
def layer(layer_tree):
    yield MetacityLayer(layer_tree)


@pytest.fixture(scope="function")
def grid(layer):
    rg = RegularGrid(layer.dir)
    yield rg

######################################
# MODLES
######################################

@pytest.fixture(scope="function")
def random_facet_model(random_vertices_normals, random_semantics, random_semantic_meta):
    model = facets.FacetModel()
    vertices, normals = random_vertices_normals
    model.vertices = vertices.flatten()
    model.normals = normals.flatten()
    model.semantics = random_semantics
    model.meta = random_semantic_meta
    return model


@pytest.fixture(scope="function")
def random_line_model(random_vertices, random_semantics, random_semantic_meta):
    model = lines.LineModel()
    model.vertices = random_vertices.flatten()
    model.semantics = random_semantics
    model.meta = random_semantic_meta
    return model


@pytest.fixture(scope="function")
def random_point_model(random_vertices, random_semantics, random_semantic_meta):
    model = points.PointModel()
    model.vertices = random_vertices.flatten()
    model.semantics = random_semantics
    model.meta = random_semantic_meta
    return model


######################################
# FILESYSTEM
######################################


@pytest.fixture(scope="function")
def geometry_tree(tmpdir_factory):
    root = tmpdir_factory.mktemp("geometry")
    yield root


@pytest.fixture(scope="function")
def layer_tree(tmpdir_factory):
    root = tmpdir_factory.mktemp("layer")
    yield root


@pytest.fixture(scope="function")
def grid_tree(tmpdir_factory):
    root = tmpdir_factory.mktemp("grid")
    yield root

