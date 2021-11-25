from metacity.io.parse import parse
from tests.conftest import project_tree, geojson_dataset
from metacity.datamodel import project
import os


def test_geojson(project_tree: str, geojson_dataset: str):
    objects = parse(geojson_dataset)
    assert len(objects) == 14

    p = project.Project(os.path.join(project_tree, 'test_project'))
    l = p.create_layer('test_layer')
    for o in objects:
        l.add(o)

    assert l.size == 14





    


