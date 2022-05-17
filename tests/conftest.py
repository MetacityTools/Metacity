import os

import metacity.utils.bbox as bbox
import numpy as np
import pytest


######################################
# GEOMETRY
######################################

def gen_random_integers(count=30):
    return np.random.randint(0, 100, count).astype(np.int32)

@pytest.fixture(scope='function')
def random_integers():
    return gen_random_integers()

def gen_random_vertices(count=30):
    coordinates = np.random.rand(count, 3).astype(np.float32) * 1000
    return coordinates


@pytest.fixture(scope="function")
def random_vertices():
    yield gen_random_vertices()


def gen_random_bbox():
    return bbox.vertices_bbox(gen_random_vertices())


@pytest.fixture(scope="function")
def random_bbox():
    yield gen_random_bbox()


def gen_random_bboxes():
    return [bbox.vertices_bbox(gen_random_vertices()) for i in range(30)]


@pytest.fixture(scope="function")
def random_bboxes():
    yield gen_random_bboxes()


######################################
# DATASETS
######################################


def data_dir():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    return package_dir

@pytest.fixture(scope='function')
def railway_dataset():
    dataset_path = os.path.join(data_dir(), 'data', 'city.json')
    yield dataset_path

@pytest.fixture(scope='function')
def geojson_dataset():
    dataset_path = os.path.join(data_dir(), 'data', 'geo.json')
    yield dataset_path

@pytest.fixture(scope='function')
def shp_line_dataset():
    dataset_path = os.path.join(data_dir(), 'data', 'shp-line', 'DOP_Cyklotrasy_l.shp')
    yield dataset_path

@pytest.fixture(scope='function')
def shp_poly_dataset():
    dataset_path = os.path.join(data_dir(), 'data', 'shp-poly', 'BD3_Prah96_mp.shp')
    yield dataset_path

@pytest.fixture(scope='function')
def data_directory():
    yield data_dir()

class DatasetStats:
    def __init__(self):
        self.obj_count = 0
        self.gtypes = {}

@pytest.fixture(scope='function')
def railway_dataset_stats():
    stats = DatasetStats()
    stats.obj_count = 121
    stats.gtypes = {
        'multisurface': 104,
        'geometryinstance': 15,
        'compositesurface': 1,
    }

    yield stats

@pytest.fixture(scope="function")
def tmp_directory(tmpdir_factory):
    dir = tmpdir_factory.mktemp("tmp_directory")
    return dir



