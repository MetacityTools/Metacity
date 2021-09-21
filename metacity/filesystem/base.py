import os
import shutil
import ntpath

METADATA = "metadata"
GEOMETRY = "geometry"
GRID = "grid"
ORIGINAL = "original"
GRID_TILES = "tiles"
GRID_CACHE = "cache"

BASE_DIRS = [METADATA, GEOMETRY, ORIGINAL,
             os.path.join(GRID, GRID_TILES), os.path.join(GRID, GRID_CACHE)]


# basics
def filename(file_path):
    return ntpath.basename(file_path)


def create_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def recreate_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    create_dir_if_not_exists(dir)


def file_exists(file):
    return os.path.exists(file)


def metadata_for_oid(meta_path, oid: str):
    return os.path.join(meta_path, oid + '.json')


def path_to_object(geometry_path, oid):
    return os.path.join(geometry_path, oid)


def path_to_model(object_path, model):
    return os.path.join(object_path, model)


def object_models(geometry_path, oid):
    object_dir = path_to_object(geometry_path, oid)
    for model in os.listdir(object_dir):
        yield os.path.join(geometry_path, oid, model)


def objects(geometry_path):
    for o in os.listdir(geometry_path):
        yield o

def remove_dirtree(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

def remove_file(path):
    if os.path.exists(path):  
        os.remove(path)