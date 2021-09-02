from metacity.grid import build
from metacity.utils.bbox import bboxes_bbox
import numpy as np


def test_generate_layout(grid, random_bbox):
    build.generate_layout(grid, random_bbox, 20)

    bboxes = []
    for tile in grid.tiles:
        bboxes.append(tile.bbox)

    assert_limits(random_bbox, bboxes)
    assert_coverage(random_bbox, bboxes)


def assert_limits(random_bbox, bboxes):
    bbox = bboxes_bbox(bboxes)
    diff = random_bbox - bbox
    assert np.all(diff < 20)


def can_join_x(jb, b):
    if b[0][1] == jb[0][1] and (b[0][0] == jb[1][0] or b[1][0] == jb[0][0]):
        return True
    return False


def can_join_y(jb, b):
    if b[0][0] == jb[0][0] and (b[0][1] == jb[1][1] or b[1][1] == jb[0][1]):
        return True        
    return False


def join(a, b):
    return bboxes_bbox([a, b])


def area(bbox):
    return (bbox[1][0] - bbox[0][0]) * (bbox[1][1] - bbox[0][1])


def estimate_tile_size(bbox, x, y):
    return (bbox[1][0] - bbox[0][0]) / x, (bbox[1][1] - bbox[0][1]) / y


def inss(l):
    """
    Insert sort for bounding boxes, alphabetical sort
    """
    nl = []
    for bb in l:
        insi = len(nl)
        for i, b in enumerate(nl):
            if bb[0][0] < b[0][0] and bb[0][1] <= b[0][1]:
                insi = i
                break
        nl.insert(insi, bb)
    return nl


def jnb(sorted_bboxes, joiner_cond):
    """
    Join sorted bounding boxes if condition is true
    """
    joined_boxes = []
    for b in sorted_bboxes:
        to_remove = []
        for bb in joined_boxes:
            if joiner_cond(b, bb):
                b = join(b, bb).tolist()
                to_remove.append(bb)
        for bb in to_remove:
            joined_boxes.remove(bb)
        joined_boxes.append(b)
    return joined_boxes


def assert_coverage(random_bbox, bboxes):
    bboxes = [box.tolist() for box in bboxes]
    sorted_bboxes = inss(bboxes)
    joined_boxes = jnb(sorted_bboxes, can_join_x)
    est_dim_y = len(joined_boxes)
    sorted_bboxes = inss(joined_boxes)
    joined_boxes = jnb(sorted_bboxes, can_join_y)
    est_dim_x = float(len(bboxes)) / est_dim_y

    assert est_dim_x.is_integer()
    # tiles do not overlap and coincide with each other
    assert len(joined_boxes) == 1
    # tiles cover the entire bbox
    assert area(joined_boxes[0]) >= area(random_bbox)  
    est_x, est_y = estimate_tile_size(joined_boxes[0], est_dim_x, est_dim_y)
    margin = est_x * est_y * (est_dim_x + est_dim_y + 1)
    # the extra padding on edge tiles is not too big
    assert area(joined_boxes[0]) - area(random_bbox) < margin 
