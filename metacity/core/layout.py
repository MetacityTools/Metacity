from typing import Union
from metacity.core.grid.grid import Grid
from metacity.core.grid.set import Tile
from metacity.core.styles.style import Style
from metacity.datamodel.layer import Layer, LayerOverlay
from metacity.filesystem import layer as fs
from metacity.datamodel.project import Project
from metacity.utils.bbox import join_boxes


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
    return {
        'tile_size': grid.tile_size,
        'tiles': [ tile_layout(tile) for tile in grid.tiles ]
    }


def layer_layout(layer: Layer):
    grid = Grid(layer)
    if grid.init and not layer.disabled:
        return {
            'name': layer.name,
            'layout': grid_layout(grid),
            'size': layer.size,
            'init': grid.init,
            'disabled': layer.disabled,
            'type': 'layer'
        }
    else:
        return {
            'name': layer.name,
            'init': grid.init,
            'disabled': layer.disabled,
            'type': 'layer'
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
