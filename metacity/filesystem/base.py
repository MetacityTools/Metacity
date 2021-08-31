import os
import shutil
from metacity.filesystem.file import id_from_filename
from metacity.datamodel.primitives import points, lines, facets


METADATA = "metadata"
GEOMETRY = "geometry"
GRID = "grid"
ORIGINAL = "original"
GRID_CACHE = os.path.join(GRID, "cache")
GRID_TILES = os.path.join(GRID, "tiles")

BASE_DIRS = [ METADATA, GEOMETRY, ORIGINAL,
             GRID, GRID_CACHE, GRID_TILES ]



PRIMITIVES = [  points.PointModel.TYPE, 
                lines.LineModel.TYPE, 
                facets.FacetModel.TYPE ] #TODO can be improved


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
        path = os.path.join(base, primitive)
        create_dir_if_not_exists(path)
        recreate_lod_dirs(path)


def file_exists(file):
    return os.path.exists(file)


def geometry_tree(base_dir):
    return [ os.path.join(base_dir, primitive, str(lod)) for lod in range(0, 5) for primitive in os.listdir(base_dir) ]


def metadata_for_oid(meta_path, oid: str):
    return os.path.join(meta_path, oid + '.json')


def path_to_object(geometry_path, oid):
    return os.path.join(geometry_path, oid)


def path_to_model(path, model):
    return os.path.join(path, model)


def object_models(geometry_path, oid):
    object_dir = os.path.join(geometry_path, oid)
    for model in os.listdir(object_dir):
        yield model


def objects(base_dir):
    oids = set()
    for dir in geometry_tree(base_dir):
        for o in os.listdir(dir):
            oid = id_from_filename(o)
            if oid not in oids:
                oids.add(oid)
                yield oid