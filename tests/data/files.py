import os

import pytest
from metacity.filesystem.base import recreate_geometry_tree


@pytest.fixture(scope="session")
def geometry_tree(tmpdir_factory):
    root = tmpdir_factory.mktemp("geometry")
    recreate_geometry_tree(root)
    return root


def data_dir():
    package_dir = os.path.dirname(os.path.realpath(__file__))
    return package_dir
    

class DatasetStats:
    def __init__(self):
        self.obj_count = 0
        self.gtypes = {}


@pytest.fixture(scope='session')
def railway_dataset():
    dataset_path = os.path.join(data_dir(), 'cityjson', 'dataset.json')
    return dataset_path


@pytest.fixture(scope='session')
def railway_dataset_stats():
    stats = DatasetStats()
    stats.obj_count = 121
    stats.gtypes = {
        'multisurface' : 104,
        'geometryinstance' : 15,
        'compositesurface' : 1
    }

    return stats
    