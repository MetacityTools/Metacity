import itertools

from metacity.io.cityjson.geometry.multisurface import (CJMultiSurface,
                                                        CJSurface)


def ensure_iterable(data):
    try:
        _ = iter(data)
        return data
    except TypeError:
        return [data]


class CJSolid(CJMultiSurface):
    def __init__(self, data, vertices):
        super().__init__(data, vertices)

    def parse(self, boundaries, semantics, vertices):
        surface = CJSurface()
        models = itertools.zip_longest(boundaries, ensure_iterable(semantics))
        for shell, shell_semantics in models:
            s = super().parse(shell, shell_semantics, vertices)
            surface.join(s)
        return surface
