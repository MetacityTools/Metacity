import numpy as np
from metacity.datamodel.primitives import points



def test_init():
    model = points.PointModel()
    assert model.vertices.shape == (0,)
    assert model.semantics.shape == (0,)
    assert len(model.meta) == 0


def test_items(random_point_model):
    model = random_point_model

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

    

def test_serialize(random_point_model):
    model = random_point_model
    data = model.serialize()
    model2 = points.PointModel()
    model2.deserialize(data)

    assert np.all(model.vertices == model2.vertices)
    assert np.all(model.semantics == model2.semantics)
    assert model.meta == model2.meta



def test_untested_props():
    model = points.PointModel()
    assert model.slicer == None
    assert model.joiner == None