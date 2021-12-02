from metacity.datamodel.layer import Layer, LayerOverlay
from metacity.core.grid.grid import Grid
from metacity.core.timeline import Timeline


def build_overlay(overlay: LayerOverlay, source: Layer, target: Layer, iterationCallback=None):
    if source.type != "layer" or target.type != "layer":
        raise Exception(f"Cannot map type {source.type} to {target.type}, only layer to layer is supported")

    build_overlay_grid(overlay, source, target, iterationCallback)
    build_overlay_timeline(overlay, source, target, iterationCallback)
    overlay.source_layer = source.name
    overlay.target_layer = target.name
    overlay.size_source = source.size
    overlay.size_target = target.size


def build_overlay_timeline(overlay, source, target, iterationCallback):
    tg = Grid(target)
    polygons = [tile.polygon for tile in tg.tiles if tile.polygon is not None]
    tl = Timeline(overlay)

    it = 0
    for oid, object in enumerate(source.objects):
        for model in object.models:
            if model.type == "timepoint":
                model.map(polygons)
                tl.add(oid, model)

        if iterationCallback is not None:
            iterationCallback(it)
            it += 1
    
    tl.persist()


def build_overlay_grid(overlay, source, target, iterationCallback):
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
