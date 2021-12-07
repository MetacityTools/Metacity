from metacity.datamodel.layer import Layer
from itertools import repeat
from metacity.datamodel.project import Project
from metacity.filesystem import layer as fs
from metacity.io.parse import parse
from metacity.core.grid.grid import build_grid
from metacity.core.timeline import build_timeline
from metacity.core.layout import build_layout
from metacity.core.mapper import build_overlay
from multiprocessing import get_context

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
        #the set does not have to be loaded since it's cleared in layer.clear()
        layer = project.get_layer(layer_name, load_set=False)
    except:
        return
    
    update = lambda it: print(f"{layer_name}:", it)
    print(f"clearing layer {layer.name}")
    layer.clear()
    print("parsing files")
    parse_original_files(layer)
    print("building grid")
    build_grid(layer, progressCallback=update)
    print("building timeline")
    build_timeline(layer, progressCallback=update)
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
    build_overlay(overlay, source, target, progressCallback=update)


def migrate(project: Project):
    print(f"Migrating project {project.dir}...")
    names = project.layer_names

    with get_context("spawn").Pool(4) as pool:
        pool.starmap(migrate_layer, zip(repeat(project), names))
        #pool.starmap(migrate_overlay, zip(repeat(project), names))
    for name in names:
        migrate_overlay(project, name)

    print("building layout")
    build_layout(project)

