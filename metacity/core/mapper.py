from metacity.datamodel.layer import Layer, LayerOverlay
from metacity.core.grid.grid import Grid
from metacity.core.timeline import Timeline
from metacity.geometry import MultiTimePointMapper, MultiTimePoint


def build_overlay(overlay: LayerOverlay, source: Layer, target: Layer, progressCallback=None):
    if source.type != "layer" or target.type != "layer":
        raise Exception(f"Cannot map type {source.type} to {target.type}, only layer to layer is supported")

    build_overlay_grid(overlay, source, target, progressCallback)
    build_overlay_timeline(overlay, source, target, progressCallback)
    overlay.source_layer = source.name
    overlay.target_layer = target.name
    overlay.size_source = source.size
    overlay.size_target = target.size
    overlay.persist()


def build_overlay_timeline(overlay: LayerOverlay, source: Layer, target: Layer, progressCallback):
    tg = Grid(target)
    polygons = [tile.polygon for tile in tg.tiles if tile.polygon is not None]
    mapper = MultiTimePointMapper(polygons)
    tl = Timeline(overlay)

    it = 0

    source_model: MultiTimePoint
    source_copy: MultiTimePoint
    for oid, source_object in enumerate(source.objects):
        for source_model in source_object.models:
            if source_model.type == "timepoint":
                source_copy = source_model.copy()
                source_copy.map(mapper)
                tl.add(oid, source_copy)

        if progressCallback is not None:
            progressCallback(f"inserting {it} to timeline")
            it += 1
    
    tl.persist(progressCallback) #persist with empty cache


def build_overlay_grid(overlay: LayerOverlay, source: Layer, target: Layer, progressCallback):
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

        if progressCallback is not None:
            progressCallback(f"mapping tile {it}")
            it += 1

    grid.persist(progressCallback) #persist with empty cache
