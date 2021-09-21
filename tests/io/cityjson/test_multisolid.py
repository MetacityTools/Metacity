import numpy as np
from metacity.io.cityjson.geometry.geometry import CJGeometry
from tests.io.cityjson.test_cityjson import assert_no_semantics

V_PER_FACE = 3 * 2
FACES = 6
CUBES = 2


def test_multisolid_all_defined(cubes_multisolid):
    vertices, data = cubes_multisolid

    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive
    
    assert geometry.type == "multisolid"
    assert len(primitive.vertices) // 3 == FACES * V_PER_FACE * CUBES
    assert len(primitive.vertices) // 3 == len(primitive.semantics)
    repeats = [V_PER_FACE for _ in range(FACES * CUBES)]
    assert np.all(np.repeat(data["semantics"]["values"], repeats) == primitive.semantics)


def test_multisolid_some_semantics_not_defined(cubes_multisolid):
    vertices, data = cubes_multisolid
    data["semantics"]["values"][0] = [ None ]
    
    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive

    assert np.all(primitive.semantics[:V_PER_FACE * FACES] == -1)
    assert np.all(primitive.semantics[V_PER_FACE * FACES:] != -1)


def test_multisolid_no_semantics(cubes_multisolid):
    vertices, data = cubes_multisolid
    data["semantics"]["values"] = None

    assert_no_semantics(data, vertices)

