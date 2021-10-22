import os
import shutil
import ntpath

METADATA = "metadata"
REGROUPED = "regrouped"
MODELS = "models"
GRID = "grid"
ORIGINAL = "original"
GRID_TILES = "tiles"
GRID_CACHE = "cache"

BASE_DIRS = [METADATA, MODELS, ORIGINAL,
             os.path.join(GRID, GRID_TILES), os.path.join(GRID, GRID_CACHE)]

OVERLAY_DIRS = [os.path.join(GRID, GRID_TILES), os.path.join(GRID, GRID_CACHE)]

# basics
def filename(file_path):
    return ntpath.basename(file_path)


def create_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


# TODO remove function
def recreate_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    create_dir_if_not_exists(dir)


def file_exists(file):
    return os.path.exists(file)


def remove_dirtree(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)


def remove_file(path):
    if os.path.exists(path):  
        os.remove(path)


def project_layout(project_dir):
    return os.path.join(project_dir, 'layout.json')