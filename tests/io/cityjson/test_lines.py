import numpy as np
from metacity.io.cityjson.parser import CJGeometry
from tests.data.cityjson import random_lines



def test_lines_all_defined():
    segments = [12, 12, 12, 12, 12]
    vertices, data = random_lines(segments=segments)

    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive
    
    repeats = np.array(segments) * 2 - 2
    assert len(primitive.vertices) // 3 == sum(repeats)
    assert np.all(np.repeat(data["semantics"]["values"], repeats) == primitive.semantics)
    assert geometry.type == "multilinestring"
    assert len(primitive.vertices) // 3 == len(primitive.semantics)


def test_lines_some_semantics_not_defined():
    segments = [12, 12, 12, 12, 12]
    vertices, data = random_lines(segments=segments)
    data["semantics"]["values"][1] = None
    
    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive

    assert np.all(primitive.semantics[0:22] != -1)
    assert np.all(primitive.semantics[22:44] == -1)
    assert np.all(primitive.semantics[44:] != -1)


def test_lines_no_semantics():
    segments = [12, 12, 12, 12, 12]
    vertices, data = random_lines(segments=segments)
    data["semantics"]["values"] = None

    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive

    assert np.all(primitive.semantics == -1)
    assert len(primitive.semantics) == len(primitive.vertices) // 3

    del data["semantics"]
    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive

    assert np.all(primitive.semantics == -1)
    assert len(primitive.semantics) == len(primitive.vertices) // 3
