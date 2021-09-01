import itertools
from metacity.io.cityjson.geometry.solid import (CJSolid, CJSurface,
                                                 ensure_iterable)


class CJMultiSolid(CJSolid):
    def __init__(self, data, vertices):
        super().__init__(data, vertices)

    def parse(self, boundaries, semantics, vertices):
        surface = CJSurface()
        models = itertools.zip_longest(boundaries, ensure_iterable(semantics))
        for solid, solid_semantic in models:
            s = super().parse(solid, solid_semantic, vertices)
            surface.join(s)

        return surface
