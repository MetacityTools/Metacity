import os

import numpy as np
import pytest


######################################
# DATASETS
######################################


def data_dir():
    package_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'testdata')
    return package_dir


def geometry_dir():
    package_dir = os.path.join(data_dir(), 'geometry')
    return package_dir


def graph_dir():
    package_dir = os.path.join(data_dir(), 'graph')
    return package_dir


@pytest.fixture(scope='function')
def geojson_dataset():
    dataset_path = os.path.join(geometry_dir(), 'geo.json')
    yield dataset_path


@pytest.fixture(scope='function')
def shp_line_dataset():
    dataset_path = os.path.join(geometry_dir(), 'shp-line', 'DOP_Cyklotrasy_l.shp')
    yield dataset_path


@pytest.fixture(scope='function')
def shp_poly_dataset():
    dataset_path = os.path.join(geometry_dir(), 'shp-poly', 'BD3_Prah96_mp.shp')
    yield dataset_path


@pytest.fixture(scope='function')
def graph_nodes_dataset():
    dataset_path = os.path.join(graph_dir(), 'sanmarino_nodes.json')
    yield dataset_path


@pytest.fixture(scope='function')
def graph_edges_dataset():
    dataset_path = os.path.join(graph_dir(), 'sanmarino_edges.json')
    yield dataset_path


@pytest.fixture(scope='function')
def geometry_directory():
    yield geometry_dir()


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
    dir = str(tmpdir_factory.mktemp("tmp_directory"))
    return dir



