from collections import defaultdict

import numpy as np
from metacity.io.cityjson.geometry.geometry import CJGeometry
from metacity.io.cityjson.parser import CJParser
from tests.data.files import (DatasetStats, railway_dataset,
                              railway_dataset_stats)


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


def assert_no_semantics(data, vertices):
    geometry = CJGeometry(data, vertices, None)
    primitiveA = geometry.primitive

    assert np.all(primitiveA.semantics == -1)
    assert len(primitiveA.semantics) == len(primitiveA.vertices) // 3

    del data["semantics"]
    geometry = CJGeometry(data, vertices, None)
    primitiveB = geometry.primitive

    assert np.all(primitiveB.semantics == -1)
    assert len(primitiveB.semantics) == len(primitiveB.vertices) // 3

    return primitiveA, primitiveB
