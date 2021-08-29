from metacity.dirtree.base import recreate_geometry_tree
import pytest


@pytest.fixture(scope="session")
def geometry_tree(tmpdir_factory):
    root = tmpdir_factory.mktemp("geometry")
    recreate_geometry_tree(root)
    return root