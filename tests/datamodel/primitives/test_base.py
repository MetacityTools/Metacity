from metacity.utils.bbox import empty_bbox
import numpy as np
from metacity.datamodel.primitives import base


def test_init():
    model = base.BaseModel()
    assert model.buffers.vertices.shape == (0,)
    assert model.buffers.semantics.shape == (0,)
    assert len(model.meta) == 0


def test_exists():
    model = base.BaseModel()
    assert model.exists == False
    model.buffers.vertices.set(np.array([4.4, 5.5, 6.6]))
    assert model.exists == True


def test_empty():
    model = base.BaseModel()
    assert model.empty == True
    model.buffers.vertices.set(np.array([4.4, 5.5, 6.6]))
    assert model.empty == False


def test_has_semantics():
    model = base.BaseModel()
    assert model.has_semantics == False
    model.buffers.semantics.set(np.array([4, 5, 6]))
    assert model.has_semantics == True


def test_bbox():
    model = base.BaseModel()
    assert np.all(model.bbox == empty_bbox())
    vertex = [4.4, 5.5, 6.6]
    model.buffers.vertices.set(np.array(vertex))
    assert np.all(model.bbox == [vertex, vertex])


def test_join():
    model = base.BaseModel()
    model.buffers.semantics.set(np.array([4, 5, 6]))

    assert model.has_semantics == True
    

def test_serialize(random_vertices, random_semantics, random_semantic_meta):
    model = base.BaseModel()   
    model.buffers.vertices.set(random_vertices.flatten())
    model.buffers.semantics.set(random_semantics.flatten())
    model.meta = random_semantic_meta
    data = model.serialize()
    model2 = base.BaseModel()
    model2.deserialize(data)

    assert np.all(model.buffers.vertices == model2.buffers.vertices)
    assert np.all(model.buffers.semantics == model2.buffers.semantics)
    assert model.buffers.keys() == model2.buffers.keys()
    assert model.meta == model2.meta
