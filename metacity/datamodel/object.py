from typing import List, Dict, Callable
from metacity.geometry import (Model, Segments, Points, Mesh)


types: Dict[str, Callable[[], Model]] = {
    Points().type: Points,
    Segments().type: Segments,
    Mesh().type: Mesh
}
"""
The types used to deserialize geometry objects.
"""


def desermodel(geometry: Model):
    """
    Deserialize a geometry object, raising an exception if the type is not supported.

    Args:
        geometry (Dict): The geometry object to deserialize.

    Returns:
        Model: The deserialized geometry object.

    Raises:
        ValueError: If the type is not supported.
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
        Serialize the object. The serialization is a dictionary with the following keys:
        ```js
        {
            // The metadata of the object.
            "meta": { "key": "value", ... },
            // The geometries of the object.
            "geometry": [ JSON, JSON, ... ]
        }
        ```

        See Also:
            :func:`metacity.geometry.Model.serialize` for the serialization of a geometry into JSON

        Returns:
            Dict: The serialized object.
        """
        return {
            "meta": self.meta,
            "geometry": [g.serialize() for g in self.geometry]
        }

    @staticmethod
    def deserialize(data: Dict):
        """
        Deserialize the object, a static method.

        Args:
            data (Dict): The data to deserialize.

        Returns:
            Object: The deserialized object.

        See Also:
            :func:`Object.serialize` for the serialization of an object into JSON
        """
        obj = Object()
        obj.meta = data["meta"]
        obj.geometry = [desermodel(g) for g in data["geometry"]]
        return obj


        
