from collections import defaultdict
from metacity.datamodel.layer.layer import Layer
from metacity.io.geojson.parser import parse


def test_geojson(layer: Layer, geojson_dataset):
    parse(layer, geojson_dataset)
    assert len(layer.object_names) == 14
    
    lengths = defaultdict(lambda: 0)
    for obj in layer.objects:
        lengths[len(obj.models.models)] += 1
        for model in obj.models.models:
            assert model.exists

    assert lengths[1] == 12
    assert lengths[6] == 2
