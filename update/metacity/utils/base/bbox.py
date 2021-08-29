import numpy as np
from typing import List


def empty_bbox():
    return np.array([[np.Infinity, np.Infinity, np.Infinity], [-np.Infinity, -np.Infinity, -np.Infinity]])


def vertices_bbox(vertices: np.ndarray):
    return np.array([np.amin(vertices, axis=0), np.amax(vertices, axis=0)])


def bboxes_bbox(bboxes: List[np.ndarray]):
    vertices = np.concatenate(bboxes)
    vertices = vertices.flatten()
    vertices = vertices.reshape((vertices.shape[0] // 3, 3))
    return np.array([np.amin(vertices[::2,:], axis=0), np.amax(vertices[1::2,:], axis=0)])


