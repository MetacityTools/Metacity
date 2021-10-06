from collections import defaultdict
from metacity.datamodel.layer.layer import Layer
from metacity.io.load import load

def test_shp(layer: Layer, shp_dataset):
    load(layer, shp_dataset)

