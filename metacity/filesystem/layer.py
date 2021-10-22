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


def create_overlay(overlay_dir):
    if not os.path.exists(overlay_dir):
        base.recreate_dir(overlay_dir)
        for dir in base.OVERLAY_DIRS:
            path = os.path.join(layer_dir, dir)
            base.create_dir_if_not_exists(path)


def layer_metadata(layer_dir: str):
    return os.path.join(layer_dir, base.METADATA)


def layer_regrouped(layer_dir: str):
    return os.path.join(layer_dir, base.REGROUPED)


def layer_models(layer_dir: str):
    return os.path.join(layer_dir, base.MODELS)


def data_set(set_dir: str, offset: int):
    return os.path.join(set_dir, str(offset))


def layer_cache(layer_dir: str):
    return os.path.join(layer_dir, base.GRID_CACHE)


def layer_tile_cache(layer_dir: str, tile_name: str):
    return os.path.join(layer_dir, base.GRID_CACHE, tile_name)


def layer_config(layer_dir: str):
    return os.path.join(layer_dir, 'config.json')


def layer_dir(project_dir: str, layer_name: str):
    return os.path.join(project_dir, layer_name)


def layer_name(layer_dir: str):
    return os.path.basename(layer_dir)


def layer_originals(layer_dir: str):
    return os.path.join(layer_dir, base.ORIGINAL)


def copy_to_layer(layer_dir: str, file_path: str):
    dst = layer_originals(layer_dir)
    return shutil.copy2(file_path, dst)


def layer_source_path(layer_dir: str, file_name: str):
    dst = layer_originals(layer_dir)
    return os.path.join(dst, file_name)


def layer_names(project_dir: str):
    #ommit hidden folders
    return [d for d in os.listdir(project_dir) if d[0] != '.']


def non_coliding_layer_dir(project_dir: str, layer_name: str):
    layer_path = layer_dir(project_dir, layer_name)
    i = 2
    while os.path.exists(layer_path):
        layer_path = layer_dir(project_dir, f"{layer_name}-{i}")
        i += 1
    return layer_path


def move_from_regrouped(layer_dir: str):
    regrouped = layer_regrouped(layer_dir)
    md = layer_metadata(layer_dir)
    rmd = layer_metadata(regrouped)
    mo = layer_models(layer_dir)
    rmo = layer_models(regrouped)
    shutil.rmtree(md)
    shutil.rmtree(mo)
    shutil.move(rmd, md)
    shutil.move(rmo, mo)
    shutil.rmtree(regrouped)


def remove(path):
    if os.path.exists(path):
        shutil.rmtree(path)