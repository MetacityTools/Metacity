from metacity.io import parse_recursively
from metacity.geometry import QuadTree


def test_build_quadtree(geometry_directory: str, tmp_directory: str):
    objects = [ o for o in parse_recursively(geometry_directory) ]
    assert len(objects) == 2826 + 5041 + 24

    max_depth = 5
    tree = QuadTree(objects, max_depth)
    tree.to_json(tmp_directory, 3)

    import os
    assert os.path.exists(os.path.join(tmp_directory, "meta.json"))
    



    

