from typing import Tuple
from metacity.datamodel.project import Project


def export_obj(project: Project, output_file: str, start: Tuple[float, float], end: Tuple[float, float]):
    written_verts = 0
    for layer in project.clayers(load_set=False):
        if layer.disabled:
            continue

        pass
        #TODO

