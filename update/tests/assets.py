import numpy as np
import metacity.geometry.bbox as bbox



## ASSETS
def random_vertices():
    coordinates = np.random.rand(30, 3).astype(np.float32) * 1000
    return coordinates


def random_vertices_normals():
    vertices = random_vertices()
    vert = vertices.reshape((vertices.shape[0] // 3, 3, 3))
    normals = []
    for a, b, c in vert:
        normals.extend(np.cross(b - a, c - a))
    
    normals = np.array(normals, dtype=np.float32)
    normals = np.repeat(normals, 3, axis=0)
    return vertices, normals


def random_semantics():
    indices = np.random.randint(0, 10, size=(30,), dtype=np.int32)
    return indices


def random_semantic_meta():
    return [{ 'attribute': 'test value' }]


def random_bboxes():
    return [ bbox.vertices_bbox(random_vertices()) for i in range(30) ]
