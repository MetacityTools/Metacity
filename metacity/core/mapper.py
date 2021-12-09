from typing import List
from metacity.datamodel.layer import Layer, LayerOverlay
from metacity.core.grid.grid import Grid
from metacity.core.timeline import Timeline
from metacity.geometry import MeshOIDMapper, MultiTimePointMapper, MultiTimePoint
from tqdm import tqdm

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



def bbox_attribute_mapping(source: Layer, target: Layer, attributes: List[str]):
    if source.type != "layer" or target.type != "layer":
        raise Exception(f"Cannot map type {source.type} to {target.type}, only layer to layer is supported")

    for o in tqdm(target.objects):
        for attribute in attributes:
            if attribute in o.meta:
                del o.meta[attribute]

    grid = Grid(target)
    tiles = [tile.polygon for tile in tqdm(grid.tiles) if tile.polygon is not None]

    mapper = MeshOIDMapper(tiles)

    grid = Grid(source)
    for tile in tqdm(grid.tiles):
        p = tile.polygon
        if p is None:
            continue
        
        mapper.map_oids(p)

    #target oid -> source oid
    mapping = mapper.mapping
    raw_mapping = mapper.raw_mapping
    with open("oid_map.txt", "w") as f:
        for oid, source_oid in tqdm(raw_mapping.items()):
            f.write("{} {}\n".format(oid, source_oid))

    target_objects = [ key for key in mapping.keys() ]
    target_objects.sort()

    for toid in tqdm(target_objects):
        source_oid = mapping[toid]
        m = source[source_oid].meta
        for attribute in attributes:
            if attribute in m:
                target[toid].meta[attribute] = m[attribute]
    
    target.persist()