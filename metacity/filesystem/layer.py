import os
from metacity.filesystem import base
import shutil


def create_project(project_dir: str):
    """
    Creates a new project directory and all the necessary subdirectories.

    Args:
        project_dir (str): The path to the project directory.
    """
    base.create_dir_if_not_exists(project_dir)
    base.create_dir_if_not_exists(os.path.join(project_dir, base.STYLES))


def create_layer(layer_dir: str):
    """
    Creates a new layer directory. If the directory already exists, it won't be overwritten. 

    Args:
        layer_dir (str): The path to the layer directory.
    """
    base.create_dir_if_not_exists(layer_dir)
    for dir in base.BASE_DIRS:
        path = os.path.join(layer_dir, dir)
        base.create_dir_if_not_exists(path)


def clear_layer(layer_dir: str, keep_originals=True):
    clear(layer_dir, keep_originals, base.BASE_DIRS)


def clear_overlay(overlay_dir: str, keep_originals=True):
    clear(overlay_dir, keep_originals, base.OVERLAY_DIRS)

def clear(base_dir, keep_originals, base_dirs):
    for dir in base_dirs:
        if dir == base.ORIGINAL and keep_originals:
            continue
        path = os.path.join(base_dir, dir)
        if os.path.exists(path):
            shutil.rmtree(path)
        base.create_dir_if_not_exists(path)


def create_overlay(overlay_dir: str):
    """
    Creates a new overlay directory. If the directory already exists, it won't be overwritten.

    Args:
        overlay_dir (str): The path to the overlay directory.
    """
    base.create_dir_if_not_exists(overlay_dir)
    for dir in base.OVERLAY_DIRS:
        path = os.path.join(overlay_dir, dir)
        base.create_dir_if_not_exists(path)


def layer_metadata(layer_dir: str):
    """
    Returns the path to the metadata directory of the layer.

    Args:
        layer_dir (str): The path to the layer directory.

    Returns:
        str: The path to the metadata directory of the layer.
    """
    return os.path.join(layer_dir, base.METADATA)


def layer_regrouped(layer_dir: str):
    """
    Returns the path to the regrouped layer directory.

    Args:
        layer_dir (str): The path to the layer directory.
    
    Returns:
        str: The path to the regrouped layer directory.
    """
    return os.path.join(layer_dir, base.REGROUPED)


def layer_models(layer_dir: str):
    return os.path.join(layer_dir, base.MODELS)


def data_set(set_dir: str, offset: int):
    return os.path.join(set_dir, str(offset))


def layer_config(layer_dir: str):
    return os.path.join(layer_dir, 'config.json')


def layer_dir(project_dir: str, layer_name: str):
    return os.path.join(project_dir, layer_name)


def overlay_dir(project_dir: str, overlay_name: str):
    return layer_dir(project_dir, overlay_name)


def layer_name(layer_dir: str):
    return os.path.basename(layer_dir)


def layer_originals(layer_dir: str):
    return os.path.join(layer_dir, base.ORIGINAL)


def layer_originals_list(layer_dir: str):
    return os.listdir(layer_originals(layer_dir))    


def layer_original_files(layer_dir: str):
    files = layer_originals_list(layer_dir)
    originals = layer_originals(layer_dir)
    return [os.path.join(originals, file) for file in files]


def copy_to_layer(layer_dir: str, file_path: str):
    dst = layer_originals(layer_dir)
    return shutil.copy2(file_path, dst)


def layer_source_path(layer_dir: str, file_name: str):
    dst = layer_originals(layer_dir)
    return os.path.join(dst, file_name)


def layer_names(project_dir: str):
    #ommit hidden folders
    return [d for d in os.listdir(project_dir) if (os.path.isdir(os.path.join(project_dir, d)) and d[0] != '.' and d not in base.RESERVED)]


def project_styles(project_dir: str):
    return os.path.join(project_dir, base.STYLES)


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