from typing import List, Dict, Callable
from metacity.geometry import (Model, Segments, Points, Mesh)


types: Dict[str, Callable[[], Model]] = {
    Points().type: Points,
    Segments().type: Segments,
    Mesh().type: Mesh
}


def desermodel(geometry):
    type = geometry["type"]
    if geometry["type"] in types:
        g = types[type]()
    else:
        raise RuntimeError(f"Unknown geometry type: {type}")
    g.deserialize(geometry)
    return g


class Object:
    def __init__(self):
        self.meta = {}
        self.geometry: List[Model] = []

    def serialize(self):
        return {
            "meta": self.meta,
            "geometry": [g.serialize() for g in self.geometry]
        }

    def deserialize(self, data):
        self.meta = data["meta"]
        self.geometry = [desermodel(g) for g in data["geometry"]]


        
