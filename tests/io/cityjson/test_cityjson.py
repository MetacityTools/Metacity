import numpy as np
from metacity.datamodel.layer.layer import Layer
from metacity.io.cityjson.geometry.geometry import CJGeometry
from metacity.io.cityjson.parser import CJParser
import json

def test_load(layer: Layer, railway_dataset, railway_dataset_stats):
    stats = railway_dataset_stats
    with open(railway_dataset, 'r') as file:
        contents = json.load(file)

    parser = CJParser(contents)
    parser.parse_and_export(layer)
    dataset_names = parser.objects.keys()

    assert parser.is_empty == False
    assert set(dataset_names) == set(layer.object_names)
    assert len(layer.object_names) == stats.obj_count
    
    for obj in layer.objects:        
        assert len(obj.models.models) == len(parser.objects[obj.oid]['geometry'])


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
