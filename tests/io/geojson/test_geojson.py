from collections import defaultdict
from metacity.io.geojson.parser import parse


def test_geojson(geojson_dataset):
    parse(geojson_dataset)
