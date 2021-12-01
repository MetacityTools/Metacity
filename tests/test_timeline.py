from metacity.core.timeline import build_timeline
from metacity.datamodel import project
from metacity.filesystem.timeline import interval
from tests.conftest import carsim_dataset, project_tree
from metacity.io.sim.parser import parse
from metacity.geometry import Interval
import os


def test_timeline(carsim_dataset: str, project_tree: str):
    objects = parse(carsim_dataset)
    project_dir = os.path.join(project_tree, 'test_project')
    layer_name = 'test_layer'

    p = project.Project(project_dir)
    l = p.create_layer(layer_name)
    for o in objects:
        l.add(o)
    l.persist()

    tl = build_timeline(l, 3600)
    for interval in tl.intervals:
        pass


