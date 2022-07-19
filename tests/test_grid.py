from metacity.datamodel.grid import Grid
from metacity.io.parse import parse


def test_grid_poly(shp_poly_dataset: str):
    objects = parse(shp_poly_dataset)
    assert len(objects) == 2826


    grid = Grid(tile_xdim=1000, tile_ydim=1000)
    assert len(grid.tiles) == 0

    for o in objects:
        grid.add_object(o)
    assert len(grid.tiles) == 6
    
    tilecounts = [len(t.objects) for t in grid.tiles.values()]

    data = grid.serialize()
    grid2 = Grid.deserialize(data)

    assert len(grid2.tiles) == 6
    tilecounts2 = [len(t.objects) for t in grid2.tiles.values()]
    assert tilecounts == tilecounts2


