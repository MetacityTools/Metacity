from metacity.datamodel.project import Project
from metacity.core.grid.grid import Grid
from metacity.core.timeline import Timeline


def cleanup(project: Project):
    for layer in project.layers:
        grid = Grid(layer)
        if grid.init:
            grid.cleanup()

        timeline = Timeline(layer)
        if timeline.init:
            timeline.cleanup()
