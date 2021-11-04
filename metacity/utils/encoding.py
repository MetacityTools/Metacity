import base64
import numpy as np


# export
def npfloat32_to_buffer(data):
    return base64.b64encode(data.astype(np.float32)).decode('utf-8')


def npint32_to_buffer(data):
    return base64.b64encode(data.astype(np.int32)).decode('utf-8')


def npuint8_to_buffer(data):
    return base64.b64encode(data.astype(np.uint8)).decode('utf-8')


# import
def base64_to_type(b64data, type):
    bdata = base64.b64decode(b64data)
    data = np.frombuffer(bdata, dtype=type)
    return data


def base64_to_float32(b64data):
    return base64_to_type(b64data, np.float32)


def base64_to_int32(b64data):
    return base64_to_type(b64data, np.int32)
