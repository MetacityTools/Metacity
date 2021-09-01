import metacity.utils.bbox as bbox
import numpy as np


##TESTS
def test_empty_bbox():
    empty = bbox.empty_bbox()
    assert np.all(empty == np.array([[np.Infinity, np.Infinity, np.Infinity], [-np.Infinity, -np.Infinity, -np.Infinity]]))


def subtest_vertices(low, high, vertices):
    for vertex in vertices:
        assert np.all(low <= vertex)
        assert np.all(high >= vertex)

    assert np.all(np.any(low == vertices, axis=0))
    assert np.all(np.any(high == vertices, axis=0))    


def test_vertices_bbox(random_vertices):
    vertices = random_vertices
    low, high = bbox.vertices_bbox(vertices)
    subtest_vertices(low, high, vertices)  
        

def test_bboxes_bbox(random_bboxes):
    bboxes = random_bboxes
    low, high = bbox.bboxes_bbox(bboxes)
    vertices = np.reshape(bboxes, (len(bboxes) * 2, 3))
    subtest_vertices(low, high, vertices)     