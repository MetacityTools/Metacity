from tests.io.cityjson.test_cityjson import assert_no_semantics
import numpy as np
from metacity.io.cityjson.geometry.geometry import CJGeometry



def test_lines_all_defined(random_lines):
    vertices, data = random_lines

    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive
    
    segments = [12, 12, 12, 12, 12]
    repeats = np.array(segments) * 2 - 2
    assert len(primitive.vertices) // 3 == sum(repeats)
    assert np.all(np.repeat(data["semantics"]["values"], repeats) == primitive.semantics)
    assert geometry.type == "multilinestring"
    assert len(primitive.vertices) // 3 == len(primitive.semantics)


def test_lines_some_semantics_not_defined(random_lines):
    vertices, data = random_lines
    data["semantics"]["values"][1] = None
    
    geometry = CJGeometry(data, vertices, None)
    primitive = geometry.primitive

    assert np.all(primitive.semantics[0:22] != -1)
    assert np.all(primitive.semantics[22:44] == -1)
    assert np.all(primitive.semantics[44:] != -1)


def test_lines_no_semantics(random_lines):
    vertices, data = random_lines
    data["semantics"]["values"] = None

    assert_no_semantics(data, vertices)

