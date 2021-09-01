import numpy as np
from metacity.datamodel.primitives import facets


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


def test_items(random_facet_model):
    model = random_facet_model

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

    

def test_serialize(random_facet_model):
    model = random_facet_model
    data = model.serialize()
    model2 = facets.FacetModel()
    model2.deserialize(data)
    models_equal(model, model2)


def test_untested_props():
    model = facets.FacetModel() 
    assert model.slicer == None