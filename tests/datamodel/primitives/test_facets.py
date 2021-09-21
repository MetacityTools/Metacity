import numpy as np
from metacity.datamodel.primitives import facets
import bisect

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
    ouv = [[3.0,   0.0,  0.0,   
            2.0,   1.0,  0.0,
            2.0,   0.0,  0.0],
           [1.0,   2.0,  0.0,
            1.0,   1.5,  0.0,
            1.5,   1.5,  0.0],
           [1.0,   1.5,  0.0,
            1.0,   0.0,  0.0,
            2.0,   1.0,  0.0,
            1.0,   1.5,  0.0,
            2.0,   1.0,  0.0,
            1.5,   1.5,  0.0,
            2.0,   1.0,  0.0,
            1.0,   0.0,  0.0,
            2.0,   0.0,  0.0],
           [0.0,   0.0,  0.0,
            0.75,  1.5,  0.0,
            0.0,   1.5,  0.0,
            0.75,  1.5,  0.0,
            0.0,   0.0,  0.0,   
            1.0,   0.0,  0.0,
            0.75,  1.5,  0.0,   
            1.0,   0.0,  0.0,   
            1.0,   1.5,  0.0],
           [0.75,  1.5,  0.0,
            1.0,   2.0,  0.0,
            0.0,   1.5,  0.0,
            1.0,   2.0,  0.0,
            0.0,   3.0,  0.0,   
            0.0,   1.5,  0.0, 
            1.0,   2.0,  0.0,   
            0.75,  1.5,  0.0,   
            1.0,   1.5,  0.0]]

    model = facets.FacetModel()
    model.buffers.vertices.set(inv)
    model.buffers.normals.set(inn)
    model.buffers.semantics.set(ins)
    
    splitted = model.split(x_planes, y_planes)
    
    occupied_semgments = set()
    for partition, ovs in zip(splitted, ouv):
        assert_unique_partition(x_planes, y_planes, occupied_semgments, ovs)
        assert np.all(partition.buffers.vertices.data == ovs)
        
        nv = len(ovs) // 3
        oun = np.array([0.0,   0.0,  1.0] * nv, dtype=np.float32)
        ous = np.array([0] * nv, dtype=np.int32)
        
        assert np.all(partition.buffers.normals.data == oun)
        assert np.all(partition.buffers.semantics.data == ous)


def assert_unique_partition(x_planes, y_planes, occupied_semgments, ovs):
    xs = []
    ys = []
    for t in np.array(ovs).reshape(len(ovs) // 9, 3, 3):
        center = np.sum(t, axis=0) / 3
        for x, y in zip(center[::3], center[1::3]):
            xs.append(bisect.bisect_left(x_planes, x))
            ys.append(bisect.bisect_left(y_planes, y))
        
    assert all(x==xs[0] for x in xs)
    assert all(y==ys[0] for y in ys)
    assert (x, y) not in occupied_semgments
    occupied_semgments.add((x, y))


def test_serialize(random_facet_model):
    model = random_facet_model
    data = model.serialize()
    model2 = facets.FacetModel()
    model2.deserialize(data)
    models_equal(model, model2)
