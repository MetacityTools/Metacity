import os
from metacity.filesystem import base
import shutil


def recrete_project(project_dir, load_existing):
    if os.path.exists(project_dir): 
        if not load_existing:
            shutil.rmtree(project_dir)
    else:
        os.mkdir(project_dir)


def recreate_layer(layer_dir, load_existing=True):
    if load_existing:
        base.create_dir_if_not_exists(layer_dir)
    else:
        base.recreate_dir(layer_dir)

    for dir in base.BASE_DIRS:
        path = os.path.join(layer_dir, dir)
        base.create_dir_if_not_exists(path)


def layer_metadata(layer_dir):
    return os.path.join(layer_dir, base.METADATA)


def layer_geometry(layer_dir):
    return os.path.join(layer_dir, base.GEOMETRY)


def layer_cache(layer_dir):
    return os.path.join(layer_dir, base.GRID_CACHE)


def layer_tile_cache(layer_dir, tile_name):
    return os.path.join(layer_dir, base.GRID_CACHE, tile_name)


def any_object_in_layer(layer_dir):
    geometry = os.path.join(layer_dir, base.GEOMETRY)
    for _ in base.objects(geometry):
        return True
    return False


def layer_objects(layer_dir):
    geometry = os.path.join(layer_dir, base.GEOMETRY)
    for oid in base.objects(geometry):
        yield oid


def layer_config(layer_dir):
    return os.path.join(layer_dir, 'config.json')


def layer_dir(project_dir, layer_name):
    return os.path.join(project_dir, layer_name)


def layer_originals(layer_dir):
    return os.path.join(layer_dir, base.ORIGINAL)


def copy_to_layer(layer_dir: str, file_path: str):
    dst = layer_originals(layer_dir)
    return shutil.copy2(file_path, dst)


def layer_names(project_dir):
    return [d for d in os.listdir(project_dir)]
