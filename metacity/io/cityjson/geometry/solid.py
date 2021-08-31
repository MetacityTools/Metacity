from metacity.io.cityjson.geometry.multisurface import CJSurface, CJMultiSurface
import itertools


def ensure_iterable(data):
    try:
        _ = iter(data)
        return data
    except TypeError:
        return [ data ]
    

class CJSolid(CJMultiSurface):
    def __init__(self, data, vertices):
        super().__init__(data, vertices)


    def parse(self, boundaries, semantics, vertices):
        surface = CJSurface()
        for shell, shell_semantics in itertools.zip_longest(boundaries, ensure_iterable(semantics)):
            s = super().parse(shell, shell_semantics, vertices)
            surface.join(s)
        return surface


