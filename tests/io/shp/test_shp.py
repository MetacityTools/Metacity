from collections import defaultdict
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.io.load import load

def test_shp(layer: MetacityLayer, shp_dataset):
    load(layer, shp_dataset)

