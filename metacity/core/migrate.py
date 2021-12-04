from metacity.datamodel.layer import Layer
from itertools import repeat
from metacity.datamodel.project import Project
from metacity.filesystem import layer as fs
from metacity.io.parse import parse
from metacity.core.grid.grid import build_grid
from metacity.core.timeline import build_timeline
from metacity.core.layout import build_layout
from metacity.core.mapper import build_overlay
from multiprocessing import Pool

def parse_original_files(layer: Layer):
    files = fs.layer_original_files(layer.dir)
    name = layer.name

    for i, file in enumerate(files):
        print(f"{name}: parsing files: {i}/{len(files)}")
        try:
            objects = parse(file)
            for o in objects:
                layer.add(o)
        except Exception as e:
            print(e)


def migrate_layer(project: Project, layer_name: str):
    try:
        layer = project.get_layer(layer_name)
    except:
        return
    
    update = lambda it: print(f"{layer_name}:", it)
    print(f"clearing layer {layer.name}")
    layer.clear()
    print("parsing files")
    parse_original_files(layer)
    print("building grid")
    build_grid(layer, update)
    print("building timeline")
    build_timeline(layer, update)
    layer.persist()


def migrate_overlay(project: Project, overlay_name: str):
    try:
        overlay = project.get_overlay(overlay_name)
    except:
        return
    
    update = lambda it: print(f"{overlay_name}:", it)
    print(f"clearing overlay {overlay.name}")
    overlay.clear()
    print("loading resources")
    source = project.get_layer(overlay.source_layer)
    target = project.get_layer(overlay.target_layer)
    print("mapping")
    build_overlay(overlay, source, target, update)


def migrate(project: Project):
    print(f"Migrating project {project.dir}...")
    names = project.layer_names

    pool = Pool(4)
    pool.starmap(migrate_layer, zip(repeat(project), names))
    pool.starmap(migrate_overlay, zip(repeat(project), names))

    print("building layout")
    build_layout(project)

