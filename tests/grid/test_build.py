from metacity.grid import build
from metacity.utils.bbox import bboxes_bbox
import numpy as np


def test_generate_layout(grid, random_bbox):
    build.generate_layout(grid, random_bbox, 20)

    path: str = grid.dir

    bboxes = []
    for tile in grid.tiles:
        bboxes.append(tile.bbox)

    bbox = bboxes_bbox(bboxes)
    diff = random_bbox - bbox
    assert np.all(diff < 20)
