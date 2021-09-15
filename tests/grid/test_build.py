from metacity.datamodel.layer.layer import MetacityLayer
from metacity.grid.build import build_grid
from metacity.io.cityjson.parser import parse


def test_build(layer: MetacityLayer, railway_dataset):
    parse(layer, railway_dataset)
    grid = build_grid(layer, 1000)

    objects = set()
    for tile in grid.tiles:
        for oid in tile.cache_objects(grid.dir):
            objects.add(oid)

    diff = set(layer.object_names) - objects
    for oid in diff:
        obj = layer.object(oid)
        for model in obj.models.models:
            assert model.empty


    #TODO test if all bboxes of sliced objects are inside tile bboxes
    
    for tile in grid.tiles:
        types = set()
        for model in tile.models:
            assert model.TYPE not in types
            types.add(model.TYPE)
