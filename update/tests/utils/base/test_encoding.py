import numpy as np
from metacity.utils.base import encoding as en
from tests.assets import random_vertices, random_semantics

def test_float32():
    data = random_vertices().flatten()
    buffer = en.npfloat32_to_buffer(data)
    data2 = en.base64_to_float32(buffer)
    data3 = en.base64_to_type(buffer, np.float32)
    assert np.all(data == data2)
    assert np.all(data == data3)


def test_int32():
    data = random_semantics().flatten()
    buffer = en.npint32_to_buffer(data)
    data2 = en.base64_to_int32(buffer)
    data3 = en.base64_to_type(buffer, np.int32)
    assert np.all(data == data2)
    assert np.all(data == data3)

