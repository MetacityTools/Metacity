import numpy as np
from metacity.io.cityjson.geometry.geometry import CJGeometry
from tests.io.cityjson.test_cityjson import assert_no_semantics

V_PER_FACE = 3 * 2
FACES = 6


def test_multisurface_all_defined(cube_multisurface):
    vertices, data = cube_multisurface

    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive
    
    assert geometry.type == "multisurface"
    assert len(primitive.vertices) // 3 == FACES * V_PER_FACE
    assert len(primitive.vertices) // 3 == len(primitive.semantics)
    repeats = [V_PER_FACE for _ in range(FACES)]
    assert np.all(np.repeat(data["semantics"]["values"], repeats) == primitive.semantics)


def test_multisurface_some_semantics_not_defined(cube_multisurface):
    vertices, data = cube_multisurface
    data["semantics"]["values"][1] = None
    
    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive

    assert np.all(primitive.semantics[0:V_PER_FACE] != -1)
    assert np.all(primitive.semantics[V_PER_FACE:V_PER_FACE * 2] == -1)
    assert np.all(primitive.semantics[V_PER_FACE * 2:] != -1)


def test_multisurface_no_semantics(cube_multisurface):
    vertices, data = cube_multisurface
    data["semantics"]["values"] = None
    
    assert_no_semantics(data, vertices)


