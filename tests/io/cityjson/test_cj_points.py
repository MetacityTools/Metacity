from tests.io.cityjson.test_cityjson import assert_no_semantics
import numpy as np
from metacity.io.cityjson.geometry.geometry import CJGeometry


def test_points_all_defined(random_points):
    vertices, data = random_points

    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive
    assert geometry.type == "multipoint"
    assert np.all(primitive.vertices == vertices[::2].flatten())
    assert np.all(primitive.semantics == data["semantics"]["values"])
    assert primitive.meta == data["semantics"]["surfaces"]


def test_points_some_semantics_not_defined(random_points):
    vertices, data = random_points
    data["semantics"]["values"][::2] = [None] * 15
    
    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive
    assert np.all(primitive.semantics[::2] == -1)
    assert np.all(primitive.semantics[1::2] != -1)


def test_points_no_semantics(random_points):
    vertices, data = random_points
    data["semantics"]["values"] = None

    primitiveA, primitiveB = assert_no_semantics(data, vertices)

    assert len(primitiveA.semantics) == len(data["boundaries"])
    assert len(primitiveB.semantics) == len(data["boundaries"])



