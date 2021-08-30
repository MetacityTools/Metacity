from metacity.geometry.bbox import empty_bbox
import numpy as np
from metacity.datamodel.primitives import base
from tests.data.random import random_semantics, random_vertices, random_semantic_meta


def test_init():
    model = base.BaseModel()
    assert model.vertices.shape == (0,)
    assert model.semantics.shape == (0,)
    assert len(model.meta) == 0


def test_exists():
    model = base.BaseModel()
    assert model.exists == False
    model.vertices = np.array([4.4, 5.5, 6.6])
    assert model.exists == True


def test_empty():
    model = base.BaseModel()
    assert model.empty == True
    model.vertices = np.array([4.4, 5.5, 6.6])
    assert model.empty == False


def test_has_semantics():
    model = base.BaseModel()
    assert model.has_semantics == False
    model.semantics = np.array([4, 5, 6])
    assert model.has_semantics == True


def test_bbox():
    model = base.BaseModel()
    assert np.all(model.bbox == empty_bbox())
    vertex = [4.4, 5.5, 6.6]
    model.vertices = np.array(vertex)
    assert np.all(model.bbox == [vertex, vertex])
    

def test_serialize():
    model = base.BaseModel()   
    model.vertices = random_vertices().flatten()
    model.semantics = random_semantics().flatten()
    model.meta = random_semantic_meta()
    data = model.serialize()
    model2 = base.BaseModel()
    model2.deserialize(data)

    assert np.all(model.vertices == model2.vertices)
    assert np.all(model.semantics == model2.semantics)
    assert model.meta == model2.meta


def test_untested_props():
    model = base.BaseModel() 
    assert model.items == None
    assert model.slicer == None