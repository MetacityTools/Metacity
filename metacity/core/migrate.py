from metacity.datamodel.layer import Layer
from metacity.datamodel.project import Project
from metacity.filesystem import layer as fs
from metacity.io.parse import parse
from metacity.core.grid.grid import build_grid
from metacity.core.timeline import build_timeline
from metacity.core.layout import build_layout
from metacity.core.mapper import build_overlay


def parse_original_files(layer: Layer):
    files = fs.layer_original_files(layer.dir)

    for i, file in enumerate(files):
        print(f"parsing files: {i}/{len(files)}", end="\r")
        try:
            objects = parse(file)
            for o in objects:
                layer.add(o)
        except Exception as e:
            print(e)


def migrate(project: Project):
    print(f"Migrating project {project.dir}...")
    update = lambda it: print(it, end="\r")
    for layer in project.layers_only:
        print(f"clearing layer {layer.name}")
        layer.clear()
        print("parsing files")
        parse_original_files(layer)
        print("building grid")
        build_grid(layer, update)
        print("building timeline")
        build_timeline(layer, update)
        layer.persist()

    for overlay in project.overlays_only:
        print(f"clearing overlay {overlay.name}")
        overlay.clear()
        print("loading resources")
        source = project.get_layer(overlay.source_layer)
        target = project.get_layer(overlay.target_layer)
        print("mapping")
        build_overlay(overlay, source, target, update)

    print("building layout")
    build_layout(project)

