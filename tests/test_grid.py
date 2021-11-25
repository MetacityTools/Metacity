from metacity.io.parse import parse
from tests.conftest import project_tree, geojson_dataset
from metacity.core.grid.grid import build_grid
from metacity.datamodel import project
from metacity.filesystem import base as fs 
import os


def test_grid(project_tree: str, geojson_dataset: str):
    objects = parse(geojson_dataset)
    assert len(objects) == 14
    project_dir = os.path.join(project_tree, 'test_project')
    layer_name = 'test_layer'
    grid_dir = os.path.join(project_dir, layer_name, fs.GRID, fs.GRID_TILES)

    p = project.Project(project_dir)
    l = p.create_layer('test_layer')
    for o in objects:
        l.add(o)
    l.persist()
    
    g = build_grid(l)

    tiles = os.listdir(grid_dir)
    assert len(tiles) == 100




    


