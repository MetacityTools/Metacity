import os
import shutil
from metacity.helpers.file import id_from_filename

METADATA = "metadata"
GEOMETRY = "geometry"
POINTS = "points"
LINES = "lines"
FACETS = "facets"
GRID = "grid"
GRID_CACHE = os.path.join(GRID, "cache")
GRID_TILES = os.path.join(GRID, "tiles")

BASE_DIRS = [ METADATA, GEOMETRY, 
             GRID, GRID_CACHE, GRID_TILES ]

PRIMITIVES = [ POINTS, LINES, FACETS ]



#basics
def create_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def recreate_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    create_dir_if_not_exists(dir)


def recreate_lod_dirs(base):
    for i in range(0, 5):
        create_dir_if_not_exists(os.path.join(base, str(i)))


def recreate_geometry_tree(base):
    for primitive in PRIMITIVES:
        path = os.join(base, primitive)
        os.mkdir(path)
        recreate_lod_dirs(path)


def geometry_tree(base_dir):
    return [ os.path.join(dir, str(i)) for i in range(0, 5) for dir in os.listdir(base_dir) ]


def metadata_for_oid(meta_path, oid: str):
    return os.path.join(meta_path, oid + '.json')


def path_to_object_lod(geometry_path, primitive, lod, oid):
    return os.path.join(geometry_path, primitive, str(lod), oid + '.json')


def objects(base_dir):
    oids = set()
    for dir in geometry_tree(base_dir):
        for o in os.listdir(dir):
            oid = id_from_filename(o)
            if oid not in oids:
                oids.add(oid)
                yield oid

