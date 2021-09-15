from metacity.io.geojson.parser import parse


def test_geojson(layer, geojson_dataset):
    parse(layer, geojson_dataset)