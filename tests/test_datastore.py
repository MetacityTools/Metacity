from metacity.datamodel.layer import Layer
from metacity.filesystem.datastore import DataStore
from metacity.io.parse import parse
import os


def test_datastore(tmp_directory: str, shp_poly_dataset: str):
    objects = parse(shp_poly_dataset)
    layer = Layer("test", tile_xdim=1000, tile_ydim=1000)
    layer.add_objects(objects)

    ds = DataStore(tmp_directory)
    ds.add_layer(layer)
    assert os.listdir(tmp_directory) == ["test"]
    
    layers = [ layer for layer in ds.layers ]
    assert len(layers) == 1
    assert len(layers[0].grid.tiles) == 6
    objcount = sum([len(t.objects) for t in layers[0].grid.tiles.values()])
    assert objcount == 2826





    