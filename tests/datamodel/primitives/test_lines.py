import numpy as np
from metacity.datamodel.primitives import lines


def test_init():
    model = lines.LineModel()
    assert model.vertices.shape == (0,)
    assert model.semantics.shape == (0,)
    assert len(model.meta) == 0


def test_items(random_line_model):
    model = random_line_model
    vertices, semantics = [], []
    for t, s in model.items:
        assert t.shape == (2, 3)
        vertices.append(t)
        assert s.shape == (2,)
        semantics.append(s)

    vertices = np.array(vertices).flatten()
    semantics = np.array(semantics).flatten()
    
    assert np.all(vertices == model.vertices)
    assert np.all(semantics == model.semantics)

    

def test_serialize(random_line_model):
    model = random_line_model
    data = model.serialize()
    model2 = lines.LineModel()
    model2.deserialize(data)

    assert np.all(model.vertices == model2.vertices)
    assert np.all(model.semantics == model2.semantics)
    assert model.meta == model2.meta



def test_untested_props():
    model = lines.LineModel() 
    assert model.slicer == None
    assert model.joiner == None