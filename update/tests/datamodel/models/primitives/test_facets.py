import numpy as np
from metacity.datamodel.primitives import facets
from tests.assets import random_vertices_normals, random_semantics, random_semantic_meta


def init_random_model():
    model = facets.FacetModel()
    vertices, normals = random_vertices_normals()
    model.vertices = vertices.flatten()
    model.normals = normals.flatten()
    model.semantics = random_semantics()
    model.meta = random_semantic_meta()
    return model


def models_equal(model, model2):
    assert np.all(model.vertices == model2.vertices)
    assert np.all(model.semantics == model2.semantics)
    assert np.all(model.normals == model2.normals)
    assert model.meta == model2.meta


def test_init():
    model = facets.FacetModel()
    assert model.vertices.shape == (0,)
    assert model.semantics.shape == (0,)
    assert model.normals.shape == (0,)
    assert len(model.meta) == 0


def test_items():
    model = init_random_model()

    vertices, normals, semantics = [], [], []
    for t, n, s in model.items:
        assert t.shape == (3, 3)
        vertices.append(t)
        assert n.shape == (3, 3)
        normals.append(n)
        assert s.shape == (3,)
        semantics.append(s)

    vertices = np.array(vertices).flatten()
    normals = np.array(normals).flatten()
    semantics = np.array(semantics).flatten()
    
    assert np.all(vertices == model.vertices)
    assert np.all(normals == model.normals)
    assert np.all(semantics == model.semantics)

    

def test_serialize():
    model = init_random_model()
    data = model.serialize()
    model2 = facets.FacetModel()
    model2.deserialize(data)
    models_equal(model, model2)


def test_untested_props():
    model = facets.FacetModel() 
    assert model.slicer == None