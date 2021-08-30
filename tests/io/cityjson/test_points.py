import numpy as np
from metacity.io.cityjson.parser import CJGeometry
from tests.data.cityjson import random_points


def test_points_all_defined():
    vertices, data = random_points()

    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive
    assert geometry.type == "multipoint"
    assert np.all(primitive.vertices == vertices[::2].flatten())
    assert np.all(primitive.semantics == data["semantics"]["values"])
    assert primitive.meta == data["semantics"]["surfaces"]


def test_points_some_semantics_not_defined():
    vertices, data = random_points()
    data["semantics"]["values"][::2] = [None] * 15
    
    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive
    assert np.all(primitive.semantics[::2] == -1)
    assert np.all(primitive.semantics[1::2] != -1)


def test_points_no_semantics():
    vertices, data = random_points()
    data["semantics"]["values"] = None

    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive
    assert np.all(primitive.semantics == -1)
    assert len(primitive.semantics) == len(data["boundaries"])

    del data["semantics"]
    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive
    assert np.all(primitive.semantics == -1)
    assert len(primitive.semantics) == len(data["boundaries"])

