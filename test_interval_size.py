from metacity.io.parse import parse
from metacity.core.timeline import build_timeline
from metacity.datamodel import project
import metacity.filesystem.timeline as fs
from metacity.filesystem.timeline import interval
from metacity.geometry import Interval
import os


def parse_data(dataset_dir: str):
    dataset_files = os.listdir(dataset_dir)

    all_objects = []
    for f in dataset_files:
        objects = parse(os.path.join(dataset_dir, f))
        for o in objects:
            all_objects.append(o)
    return all_objects

def create_timeline(dataset_dir: str, project_tree: str):
    objects = parse_data(dataset_dir)
    project_dir = os.path.join(project_tree, 'test_project')
    layer_name = 'test_layer'

    p = project.Project(project_dir)
    p.delete()
    p = project.Project(project_dir)
    l = p.create_layer(layer_name)
    for o in objects:
        l.add(o)
    l.persist()

    return(build_timeline(l, 5))


def main():

    dataset_dir = "data/car-10k"
    project_tree = "projects"
    tl = create_timeline(dataset_dir, project_tree)
    tl.persist()

if __name__ == "__main__":
    main()
