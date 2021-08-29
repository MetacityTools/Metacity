import numpy as np
from metacity.datamodel.models.primitives import points
from tests.assets import random_vertices, random_semantics, random_semantic_meta


def init_random_model():
    model = points.PointModel()
    vertices = random_vertices()
    model.vertices = vertices.flatten()
    model.semantics = random_semantics()
    model.semantics_meta = random_semantic_meta()
    return model


def test_init():
    model = points.PointModel()
    assert model.vertices.shape == (0,)
    assert model.semantics.shape == (0,)
    assert len(model.semantics_meta) == 0


def test_items():
    model = init_random_model()

    vertices, semantics = [], []
    for t, s in model.items:
        assert t.shape == (3,)
        vertices.append(t)
        assert type(s) is np.int32
        semantics.append(s)

    vertices = np.array(vertices).flatten()
    semantics = np.array(semantics).flatten()
    
    assert np.all(vertices == model.vertices)
    assert np.all(semantics == model.semantics)

    

def test_serialize():
    model = init_random_model()
    data = model.serialize()
    model2 = points.PointModel()
    model2.deserialize(data)

    assert np.all(model.vertices == model2.vertices)
    assert np.all(model.semantics == model2.semantics)
    assert model.semantics_meta == model2.semantics_meta



def test_untested_props():
    model = points.PointModel()
    assert model.slicer == None
    assert model.joiner == None