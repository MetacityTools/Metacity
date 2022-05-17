import numpy as np
from metacity.utils import encoding as en

def test_float32(random_vertices):
    data = random_vertices.flatten()
    buffer = en.npfloat32_to_buffer(data)
    data2 = en.base64_to_float32(buffer)
    data3 = en.base64_to_type(buffer, np.float32)
    assert np.all(data == data2)
    assert np.all(data == data3)


def test_int32(random_integers):
    data = random_integers.flatten()
    buffer = en.npint32_to_buffer(data)
    data2 = en.base64_to_int32(buffer)
    data3 = en.base64_to_type(buffer, np.int32)
    assert np.all(data == data2)
    assert np.all(data == data3)