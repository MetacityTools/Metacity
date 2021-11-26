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


def tile_layout(tile: Tile):
    box = join_boxes([o.bounding_box for o in tile.models])
    return {
        'box': box,
        'x': tile.x,
        'y': tile.y,
        'file': fs.base.filename(tile.file)
    }


def interval_layout(timeline: Timeline, interval: Interval):
    return {
        'start_time': interval.start_time,
        'file': tfs.interval(timeline.dir, interval.start_time)
    }


def timeline_layout(timeline: Timeline):
    if not timeline.init:
        return None

    return {
        'interval_length': timeline.group_by,
        'intervals': [ interval_layout(timeline, interval) for interval in timeline.intervals ]
    }


def grid_layout(grid: Grid):
    if not grid.init:
        return None

    return {
        'tile_size': grid.tile_size,
        'tiles': [ tile_layout(tile) for tile in grid.tiles ]
    }


def layer_layout(layer: Layer):
    grid = Grid(layer)
    timeline = Timeline(layer)
    base = {
        'name': layer.name,
        'disabled': layer.disabled,
        'type': 'layer',
        'size': layer.size,
        'grid': grid_layout(grid),
        'timeline': timeline_layout(timeline)
    }


def overlay_layout(overlay: LayerOverlay):
    grid = Grid(overlay)
    if grid.init and not overlay.disabled:
        return {
            'name': overlay.name,
            'source': overlay.source_layer,
            'target': overlay.target_layer,
            'size': overlay.size,
            'layout': grid_layout(grid),
            'init': grid.init,
            'disabled': overlay.disabled,
            'type': 'overlay'
        }
    else:
        return {
            'name': overlay.name,
            'source': overlay.source_layer,
            'target': overlay.target_layer,
            'size': overlay.size,
            'init': grid.init,
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
