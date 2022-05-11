from typing import List, Dict, Callable
from metacity.geometry import (Model, Segments, Points, Mesh)


types: Dict[str, Callable[[], Model]] = {
    Points().type: Points,
    Segments().type: Segments,
    Mesh().type: Mesh
}


def desermodel(geometry):
    """
    Deserialize a geometry object.

    Args:
        geometry (Dict): The geometry object to deserialize.
    """
    type = geometry["type"]
    if geometry["type"] in types:
        g = types[type]()
    else:
        raise RuntimeError(f"Unknown geometry type: {type}")
    g.deserialize(geometry)
    return g


class Object:
    def __init__(self):
        """
        Initialize an empty object. Each objects represents a collection of geometries and metadata.
        Single object can have multiple instances of geometry and a single dictionary of key-value pairs.
        All values in the metadata dictionary need to be serializable.
        """
        self.meta = {}
        self.geometry: List[Model] = []

    def serialize(self):
        """
        Serialize the object.

        Returns:
            Dict: The serialized object.
        """
        return {
            "meta": self.meta,
            "geometry": [g.serialize() for g in self.geometry]
        }

    def deserialize(self, data):
        """
        Deserialize the object.

        Args:
            data (Dict): The data to deserialize.
        """
        self.meta = data["meta"]
        self.geometry = [desermodel(g) for g in data["geometry"]]


        
