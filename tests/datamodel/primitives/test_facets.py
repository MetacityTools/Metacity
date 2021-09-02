import numpy as np
from metacity.datamodel.primitives import facets


def models_equal(model, model2):
    assert np.all(model.buffers.vertices == model2.buffers.vertices)
    assert np.all(model.buffers.semantics == model2.buffers.semantics)
    assert np.all(model.buffers.normals == model2.buffers.normals)
    assert model.buffers.keys() == model2.buffers.keys()
    assert model.meta == model2.meta


def test_init():
    model = facets.FacetModel()
    assert model.buffers.vertices.shape == (0,)
    assert model.buffers.semantics.shape == (0,)
    assert model.buffers.normals.shape == (0,)
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
    
    assert np.all(vertices == model.buffers.vertices)
    assert np.all(normals == model.buffers.normals)
    assert np.all(semantics == model.buffers.semantics)

    

def test_serialize(random_facet_model):
    model = random_facet_model
    data = model.serialize()
    model2 = facets.FacetModel()
    model2.deserialize(data)
    models_equal(model, model2)


def test_untested_props():
    model = facets.FacetModel() 
    assert model.slicer == None