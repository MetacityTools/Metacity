import numpy as np

def rep_nones(data):
        return [ i if i != None else -1 for i in data]


def gen_nones(elements_count):
    return [ -1 ] * elements_count


class CJBasePrimitive:
    def __init__(self, data):
        self.lod = data["lod"]

    def generate_semantics(self, elements_count):
        self.semantics = np.array(gen_nones(elements_count), dtype=np.int32)
        self.meta = []


    def transform(self):
        raise NotImplementedError(f"The CJ primitive {self} requires implementation of transform method.")