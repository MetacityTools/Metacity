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


def test_slice():
    inv = np.array([0.0, 0.0, 0.0, 
                    3.0, 0.0, 0.0, 
                    0.0, 3.0, 0.0], dtype=np.float32)
    ins = np.array([0, 0, 0], dtype=np.int32)
    inn = np.array([0.0, 0.0, 1.0, 
                    0.0, 0.0, 1.0, 
                    0.0, 0.0, 1.0], dtype=np.float32)
    x_planes = [1.0, 2.0]
    y_planes = [1.5]
    # TODO matching segments regardless of order
    ouv = [3.0,   0.0,  0.0,   
           2.0,   1.0,  0.0,
           2.0,   0.0,  0.0,
           1.0,   2.0,  0.0,
           1.0,   1.5,  0.0,
           1.5,   1.5,  0.0,
           1.0,   1.5,  0.0,
           1.0,   0.0,  0.0,
           2.0,   1.0,  0.0,
           1.0,   1.5,  0.0,
           2.0,   1.0,  0.0,
           1.5,   1.5,  0.0,
           2.0,   1.0,  0.0,
           1.0,   0.0,  0.0,
           2.0,   0.0,  0.0,
           0.0,   0.0,  0.0,
           0.75,  1.5,  0.0,
           0.0,   1.5,  0.0,
           0.75,  1.5,  0.0,
           1.0,   2.0,  0.0,
           0.0,   1.5,  0.0,
           1.0,   2.0,  0.0,
           0.0,   3.0,  0.0,   
           0.0,   1.5,  0.0, 
           1.0,   2.0,  0.0,   
           0.75,  1.5,  0.0,   
           1.0,   1.5,  0.0,
           0.75,  1.5,  0.0,
           0.0,   0.0,  0.0,   
           1.0,   0.0,  0.0,
           0.75,  1.5,  0.0,   
           1.0,   0.0,  0.0,   
           1.0,   1.5,  0.0 ]
    nv = len(ouv) // 3
    oun = np.array([0.0,   0.0,  1.0] * nv, dtype=np.float32)
    ous = np.array([0] * nv, dtype=np.int32)

    model = facets.FacetModel()
    model.buffers.vertices.set(inv)
    model.buffers.normals.set(inn)
    model.buffers.semantics.set(ins)
    splitted = model.split(x_planes, y_planes)
    for partition in splitted:
        print(partition.buffers.vertices.data)

    assert np.all(splitted.buffers.vertices.data == ouv)
    assert np.all(splitted.buffers.normals.data == oun)
    assert np.all(splitted.buffers.semantics.data == ous)  


def test_serialize(random_facet_model):
    model = random_facet_model
    data = model.serialize()
    model2 = facets.FacetModel()
    model2.deserialize(data)
    models_equal(model, model2)
