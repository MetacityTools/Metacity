from typing import Union
from metacity.core.grid.grid import Grid
from metacity.core.timeline import Timeline
from metacity.core.grid.set import Tile
from metacity.core.styles.style import Style
from metacity.datamodel.layer import Layer, LayerOverlay
from metacity.filesystem import layer as fs
from metacity.filesystem import timeline as tfs
from metacity.datamodel.project import Project
from metacity.geometry import Interval
from metacity.utils.bbox import join_boxes


def interval_layout(timeline: Timeline, interval: Interval):
    return {
        'start_time': interval.start_time,
        'file': fs.base.filename(tfs.interval(timeline.dir, interval.start_time))
    }


def timeline_layout(timeline: Timeline):
    if not timeline.init:
        return None

    intervals = [ interval_layout(timeline, interval) for interval in timeline.intervals ]

    if len(intervals) == 0:
        return None

    return {
        'interval_length': timeline.group_by,
        'intervals': intervals
    }


def tile_layout(tile: Tile):
    box = join_boxes([o.bounding_box for o in tile.models])
    return {
        'box': box,
        'x': tile.x,
        'y': tile.y,
        'file': fs.base.filename(tile.file)
    }

def grid_layout(grid: Grid):
    if not grid.init:
        return None

    tiles = [ tile_layout(tile) for tile in grid.tiles ]

    if len(tiles) == 0:
        return None

    return {
        'tile_size': grid.tile_size,
        'tiles': tiles
    }


def layer_layout(layer: Layer):
    grid = Grid(layer)
    timeline = Timeline(layer)
    return {
        'name': layer.name,
        'disabled': layer.disabled,
        'type': 'layer',
        'size': layer.size,
        'grid': grid_layout(grid),
        'timeline': timeline_layout(timeline)
    }


def overlay_layout(overlay: LayerOverlay):
    grid = Grid(overlay)
    timeline = Timeline(overlay)
    return {
        'name': overlay.name,
        'source': overlay.source_layer,
        'target': overlay.target_layer,
        'size': overlay.size,
        'grid': grid_layout(grid),
        'timeline': timeline_layout(timeline),
        'disabled': overlay.disabled,
        'type': 'overlay'
    }



def element_layout(layer: Union[Layer, LayerOverlay]):
    if layer.type == 'layer':
        return layer_layout(layer)
    elif layer.type == 'overlay':
        return overlay_layout(layer)


def style_layout(project: Project):
    return Style.list(project)


def build_layout(project: Project):
    layout_layers = []
    for layer in project.clayers(load_set=False):
        layout_layers.append(element_layout(layer))

    layout = {
        "layers": layout_layers,
        "styles": style_layout(project)
    }

    fs.base.write_json(fs.base.project_layout(project.dir), layout)
