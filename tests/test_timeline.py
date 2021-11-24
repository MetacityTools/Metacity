from metacity.core.timeline import build_timeline
from metacity.datamodel import project
from tests.conftest import carsim_dataset
from metacity.io.sim.parser import parse
from metacity.geometry import Interval
import os


def test_timeline(carsim_dataset: str):
    objects = parse(carsim_dataset)
    project_dir = os.path.join(project_tree, 'test_project')
    layer_name = 'test_layer'

    p = project.Project(project_dir)
    l = p.create_layer('test_layer')
    for o in objects:
        l.add(o)
    l.persist()

    tl = build_timeline(l)

