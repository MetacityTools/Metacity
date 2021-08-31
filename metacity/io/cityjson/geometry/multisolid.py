from metacity.io.cityjson.geometry.solid import CJSurface, CJSolid, ensure_iterable
import itertools




class CJMultiSolid(CJSolid):
    def __init__(self, data, vertices):
        super().__init__(data, vertices)


    def parse(self, boundaries, semantics, vertices):
        surface = CJSurface()
        for solid, solid_semantic in itertools.zip_longest(boundaries, ensure_iterable(semantics)):
            s = super().parse(solid, solid_semantic, vertices)
            surface.join(s)

        return surface