

class Surface:
    def __init__(self, vertices=None, normals=None, semantics=None):
        self.v = [] if vertices is None else vertices
        self.n = [] if normals is None else normals
        self.s = [] if semantics is None else semantics

    def join(self, surface):
        self.v.extend(surface.v)
        self.n.extend(surface.n)
        self.s.extend(surface.s)