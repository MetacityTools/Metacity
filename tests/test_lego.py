from metacity.io.parse import parse
from tests.conftest import project_tree, geojson_dataset, lego_tree
from metacity.core.grid.grid import build_grid
from metacity.datamodel import project
from metacity.filesystem import base as fs 
from metacity.core.legofy import legofy
import os


def test_lego(project_tree: str, geojson_dataset: str, lego_tree: str):
    objects = parse(geojson_dataset)
    assert len(objects) == 14
    project_dir = os.path.join(project_tree, 'test_project')
    layer_name = 'test_layer'

    p = project.Project(project_dir)
    l = p.create_layer('test_layer')
    for o in objects:
        l.add(o)
    l.persist()
    
    build_grid(l)
    legofy(p, lego_tree, [0, 0], [100, 100])


    