import numpy as np
import metacity.utils.bbox as bbox



## ASSETS
def random_vertices(count=30):
    coordinates = np.random.rand(count, 3).astype(np.float32) * 1000
    return coordinates


def random_vertices_normals(count=30):
    vertices = random_vertices(count)
    vert = vertices.reshape((vertices.shape[0] // 3, 3, 3))
    normals = []
    for a, b, c in vert:
        normals.extend(np.cross(b - a, c - a))
    
    normals = np.array(normals, dtype=np.float32)
    normals = np.repeat(normals, 3, axis=0)
    return vertices, normals


def random_semantics(count=30, srange=10):
    indices = np.random.randint(0, srange, size=(count,), dtype=np.int32)
    return indices


def random_semantic_meta():
    return [{ 'attribute': 'test value' }]


def random_bboxes():
    return [ bbox.vertices_bbox(random_vertices()) for i in range(30) ]
