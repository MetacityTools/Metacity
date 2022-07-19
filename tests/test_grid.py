from metacity.geometry import Grid
from metacity.io.shapefile import parse
import os

def test_grid_poly(shp_poly_dataset: str, tmp_directory: str):
    models = parse(shp_poly_dataset)
    assert len(models) == 2826

    grid = Grid(1000, 1000)
    for m in models:
        grid.add_model(m)

    g = grid.grid
    assert len(g) == 6
    tile_counts = { key: len(tile) for key, tile in g.items() }
    
    expected_counts = {(-749, -1054): 1265, (-748, -1054): 208, (-750, -1053): 318, (-749, -1053): 211, (-748, -1053): 477, (-750, -1054): 347}
    assert tile_counts == expected_counts

    grid.to_gltf(os.path.join(tmp_directory, "test.gltf"), False)
    grid.to_gltf(os.path.join(tmp_directory, "test.gltf"), True)



