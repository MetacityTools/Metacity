import os
import shutil
import json
import ntpath

METADATA = "metadata"
REGROUPED = "regrouped"
MODELS = "models"
GRID = "grid"
ORIGINAL = "original"
GRID_TILES = "tiles"
GRID_CACHE = "cache"
STYLES = "styles"


RESERVED = [STYLES]

BASE_DIRS = [METADATA, MODELS, ORIGINAL, os.path.join(GRID, GRID_TILES), os.path.join(GRID, GRID_CACHE)]

OVERLAY_DIRS = [os.path.join(GRID, GRID_TILES), os.path.join(GRID, GRID_CACHE)]

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


def rename(old, new):
    if file_exists(old) and not file_exists(new):
        os.rename(old, new)
        return True
    return False


def project_layout(project_dir):
    return os.path.join(project_dir, 'layout.json')


def readable(file):
    f = open(file, "r")
    return f.readable()


def writable(file):
    f = open(file, "w")
    return f.writable()


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)


def delete_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)


def write_json(filename, data):
    delete_file(filename)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def write_mss(filename, data):
    with open(filename, 'w') as file:
        file.write(data)


def read_mss(filename):
    with open(filename, 'r') as file:
        return file.read()


def dir_from_path(path):
    return os.path.dirname(path)


def change_suffix(path, suffix):
    base = os.path.splitext(path)[0]
    return f"{base}.{suffix}"


def get_suffix(path):
    return os.path.splitext(path)[1][1:]

def valid_name(name):
    return not (name in RESERVED)