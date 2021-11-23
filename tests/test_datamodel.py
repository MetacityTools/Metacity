from metacity.datamodel import project
from tests.conftest import project_tree
from metacity.filesystem import base as bfs
import os


def test_project(project_tree: str):
    project_name = "test_project"
    project_dir = os.path.join(project_tree, project_name)

    p = project.Project(project_dir)

    assert os.path.exists(project_dir)
    assert os.path.exists(os.path.join(project_dir, 'styles'))


def test_layers(project_tree: str):
    project_name = "test_project"
    layer_name = "test_layer"
    project_dir = os.path.join(project_tree, project_name)

    p = project.Project(project_dir)
    l1 = p.create_layer(layer_name)

    assert os.path.exists(os.path.join(project_dir, layer_name))
    assert os.path.exists(os.path.join(project_dir, layer_name, bfs.ORIGINAL))
    assert os.path.exists(os.path.join(project_dir, layer_name, bfs.METADATA))
    assert os.path.exists(os.path.join(project_dir, layer_name, bfs.MODELS))
    assert os.path.exists(os.path.join(project_dir, layer_name, bfs.GRID))
    assert os.path.exists(os.path.join(project_dir, layer_name, bfs.GRID, bfs.GRID_CACHE))
    assert os.path.exists(os.path.join(project_dir, layer_name, bfs.GRID, bfs.GRID_TILES))
    assert os.path.exists(os.path.join(project_dir, layer_name, bfs.GRID, bfs.GRID_STREAM))
    assert os.path.exists(os.path.join(project_dir, layer_name, bfs.TIMELINE))

    l2 = p.create_layer(layer_name)

    assert os.path.exists(os.path.join(project_dir, layer_name + '-2'))

    l = p.get_layer(layer_name)
    assert l.name == l1.name
    assert l1.name != l2.name

    p.delete_layer(layer_name)
    assert not os.path.exists(os.path.join(project_dir, layer_name))




def test_overlays(project_tree: str):
    project_name = "test_project"
    overlay_name = "test_layer"
    project_dir = os.path.join(project_tree, project_name)

    p = project.Project(project_dir)
    l1 = p.create_overlay(overlay_name)

    assert os.path.exists(os.path.join(project_dir, overlay_name))
    assert not os.path.exists(os.path.join(project_dir, overlay_name, bfs.ORIGINAL))
    assert not os.path.exists(os.path.join(project_dir, overlay_name, bfs.METADATA))
    assert not os.path.exists(os.path.join(project_dir, overlay_name, bfs.MODELS))
    assert os.path.exists(os.path.join(project_dir, overlay_name, bfs.GRID))
    assert os.path.exists(os.path.join(project_dir, overlay_name, bfs.GRID, bfs.GRID_CACHE))
    assert os.path.exists(os.path.join(project_dir, overlay_name, bfs.GRID, bfs.GRID_TILES))
    assert os.path.exists(os.path.join(project_dir, overlay_name, bfs.GRID, bfs.GRID_STREAM))
    assert os.path.exists(os.path.join(project_dir, overlay_name, bfs.TIMELINE))

    l2 = p.create_overlay(overlay_name)

    assert os.path.exists(os.path.join(project_dir, overlay_name + '-2'))

    l = p.get_overlay(overlay_name)
    assert l.name == l1.name
    assert l1.name != l2.name

    p.delete_overlay(overlay_name)
    assert not os.path.exists(os.path.join(project_dir, overlay_name))
