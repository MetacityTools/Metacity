from metacity.datamodel.layer import Layer, LayerOverlay
from metacity.core.grid.grid import Grid


def build_overlay(overlay: LayerOverlay, source: Layer, target: Layer, iterationCallback=None):
    if source.type != "layer" or target.type != "layer":
        raise Exception(f"Cannot map type {source.type} to {target.type}, only layer to layer is supported")

    tg = Grid(target)
    sg = Grid(source)
    grid = Grid(overlay)

    it = 0
    for source_tile, target_tile in sg.overlay(tg):
        pol = target_tile.polygon
        if pol is None:
            continue
        
        for source_model in source_tile.models:
            source_copy = source_model.copy()
            source_copy.map(pol)
            grid.tile_from_single_model(source_copy, source_tile.name)

        if iterationCallback is not None:
            iterationCallback(it)
            it += 1

    grid.persist() #persist with empty cache
    overlay.source_layer = source.name
    overlay.target_layer = target.name
    overlay.size_source = source.size
    overlay.size_target = target.size
