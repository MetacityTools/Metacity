from metacity.core.grid.grid import build_grid
from metacity.core.mapper import build_overlay
from metacity.io.parse import parse
from metacity.core.timeline import build_timeline
from metacity.datamodel import layer, project
import os

SIM_DATA_DIR = "data/car-test"
INTERVAL_LEN = 60
PROJECT_NAME = "test_project"


def parse_sim_data(dataset_dir: str):
    dataset_files = os.listdir(dataset_dir)

    all_objects = []
    for f in dataset_files:
        objects = parse(os.path.join(dataset_dir, f))
        for o in objects:
            all_objects.append(o)
    return all_objects

def layer_from_dataset(layer_name: str, dataset: str, project: project.Project, sim = False):
    objects = []
    if sim == True:
        objects = parse_sim_data(dataset)
    else:
        objects = parse(dataset)

    l = project.create_layer(layer_name)
    
    for o in objects:
        l.add(o)
    l.persist()

    return l


def test_timeline_overlay(terrain_dataset: str, project_tree: str):
    project_tree = "projects"
    project_dir = os.path.join(project_tree, PROJECT_NAME)
    p = project.Project(project_dir)
    p.delete()
    p = project.Project(project_dir)

    l1 = layer_from_dataset('terrain_layer', terrain_dataset, p)
    grid = build_grid(l1)
    l2 = layer_from_dataset('agent_car_layer', SIM_DATA_DIR, p, True)
    ol = p.create_overlay('mapped_overlay')
    
    tl = build_timeline(l2, INTERVAL_LEN)
    mappel_ol = build_overlay(ol, l2, l1)

