from tests.data.random import random_points, random_lines
from tests.data.files import DatasetStats, railway_dataset, railway_dataset_stats
from metacity.io.cityjson.parser import CJGeometry, CJParser
from collections import defaultdict
import numpy as np

def count_gtypes(parser):
    gtypes = defaultdict(lambda: 0)
    for o in parser.parsed_objects:
        for g in o.geometry:
            gtypes[g.type] += 1
    return gtypes


def test_load(railway_dataset, railway_dataset_stats: DatasetStats):
    stats = railway_dataset_stats
    parser = CJParser(railway_dataset)
    parser.parse()
    gtypes = count_gtypes(parser)
    
    assert parser.is_empty == False
    assert len(parser.parsed_objects) == stats.obj_count
    assert stats.gtypes == gtypes



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



