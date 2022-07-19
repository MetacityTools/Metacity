from metacity.geometry import Layer
from metacity.io.shapefile import parse
import os


def test_layer(tmp_directory: str, shp_poly_dataset: str):
    objects = parse(shp_poly_dataset)
    layer = Layer()

    layer.add_models(objects)
    assert layer.size == 2826

    layer.to_gltf(os.path.join(tmp_directory, "test.gltf"))

    layer2 = Layer()
    layer2.from_gltf(os.path.join(tmp_directory, "test.gltf"))
    assert layer2.size == layer.size





    