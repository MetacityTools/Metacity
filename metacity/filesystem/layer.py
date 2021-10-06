import os
from metacity.filesystem import base
import shutil


def create_project(project_dir):
    if not os.path.exists(project_dir): 
        os.mkdir(project_dir)


def create_layer(layer_dir):
    if not os.path.exists(layer_dir):
        base.recreate_dir(layer_dir)
        for dir in base.BASE_DIRS:
            path = os.path.join(layer_dir, dir)
            base.create_dir_if_not_exists(path)


def layer_metadata(layer_dir):
    return os.path.join(layer_dir, base.METADATA)


def layer_models(layer_dir):
    return os.path.join(layer_dir, base.MODELS)


def layer_object_set_model(layer_dir, offset):
    return os.path.join(layer_models(layer_dir), f"set{offset}.json")


def layer_object_set_meta(layer_dir, offset):
    return os.path.join(layer_metadata(layer_dir), f"set{offset}.json")


def layer_object_set_exists(layer_dir, offset):
    return os.path.exists(layer_object_set_model(layer_dir, offset)) \
        and os.path.exists(layer_object_set_meta(layer_dir, offset))


def layer_cache(layer_dir):
    return os.path.join(layer_dir, base.GRID_CACHE)


def layer_tile_cache(layer_dir, tile_name):
    return os.path.join(layer_dir, base.GRID_CACHE, tile_name)


def layer_config(layer_dir):
    return os.path.join(layer_dir, 'config.json')


def layer_dir(project_dir, layer_name):
    return os.path.join(project_dir, layer_name)


def layer_name(layer_dir):
    return os.path.basename(layer_dir)


def layer_originals(layer_dir):
    return os.path.join(layer_dir, base.ORIGINAL)


def copy_to_layer(layer_dir: str, file_path: str):
    dst = layer_originals(layer_dir)
    return shutil.copy2(file_path, dst)


def layer_source_path(layer_dir: str, file_name: str):
    dst = layer_originals(layer_dir)
    return os.path.join(dst, file_name)


def layer_names(project_dir):
    return [d for d in os.listdir(project_dir)]


def non_coliding_layer_dir(project_dir, layer_name):
    layer_path = layer_dir(project_dir, layer_name)
    i = 2
    while os.path.exists(layer_path):
        layer_path = layer_dir(project_dir, f"{layer_name}-{i}")
        i += 1
    return layer_path