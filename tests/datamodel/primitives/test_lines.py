import numpy as np
from metacity.datamodel.primitives import lines


def test_init():
    model = lines.LineModel()
    assert model.buffers.vertices.shape == (0,)
    assert model.buffers.semantics.shape == (0,)
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
    
    assert np.all(vertices == model.buffers.vertices)
    assert np.all(semantics == model.buffers.semantics)


def test_slice():
    inv = np.array([0.0, 0.0, 0.0, 
                    2.0, 2.0, 0.0, 
                    2.0, 2.0, 0.0, 
                    6.0, 0.0, 0.0], dtype=np.float32)
    ins = np.array([0, 0, 1, 1], dtype=np.int32)
    x_planes = [1.0, 3.0]
    y_planes = [1.0]
    # the output array is a bit scrambled
    # TODO matching segments regardless of order
    ouv = np.array([0.0, 0.0, 0.0,
                    1.0, 1.0, 0.0, 
                    1.0, 1.0, 0.0,
                    2.0, 2.0, 0.0, 
                    2.0, 2.0, 0.0, 
                    3.0, 1.5, 0.0,
                    6.0, 0.0, 0.0,
                    4.0, 1.0, 0.0,
                    4.0, 1.0, 0.0,
                    3.0, 1.5, 0.0 ], dtype=np.float32)

    ous = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1], dtype=np.int32)

    model = lines.LineModel()
    model.buffers.vertices.set(inv)
    model.buffers.semantics.set(ins)
    splitted = model.split(x_planes, y_planes)
    print(splitted.buffers.vertices.data)
    assert np.all(splitted.buffers.vertices.data == ouv)
    assert np.all(splitted.buffers.semantics.data == ous)


def test_serialize(random_line_model):
    model = random_line_model
    data = model.serialize()
    model2 = lines.LineModel()
    model2.deserialize(data)

    assert np.all(model.buffers.vertices == model2.buffers.vertices)
    assert np.all(model.buffers.semantics == model2.buffers.semantics)
    assert model.buffers.keys() == model2.buffers.keys()
    assert model.meta == model2.meta
