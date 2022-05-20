from metacity.datamodel.object import Object
from metacity.datamodel.grid import Grid
from typing import List, Dict

class Layer:
    def __init__(self, name: str, tile_xdim: float = 1000.0, tile_ydim: float = 1000.0):
        """
        Initialize a layer. Layer represents a collection of objects.
        
        Args:
            name (str): The name of the layer.
            tile_xdim (float): The x dimension of the tiles. Default is 1000.0.
            tile_ydim (float): The y dimension of the tiles. Default is 1000.0.

        Example:
            Initialize a layer with a name and a grid:

        >>> layer = Layer("layer1", 1000.0, 1000.0)
        >>> layer.name
        "layer1"
        >>> layer.grid.width
        1000.0

        """
        self.name = name
        self.grid = Grid(tile_xdim, tile_ydim)
    
    def add_object(self, obj: Object):
        """
        Add an object to the layer.
        
        Args:
            obj (Object): The object to add.

        Example:
            Add an object to the layer:

        >>> layer = Layer("layer1", 1000.0, 1000.0)
        >>> object = metacity.io.parse('single_point_object.shp')[0]
        >>> layer.add_object(object)
        >>> len(layer.grid.tiles)
        1   
        """
        self.grid.add_object(obj)

    def add_objects(self, objs: List[Object]):
        """
        Add objects to the layer. 

        Args:
            objs (List[Object]): The objects to add.
        """
        for obj in objs:
            self.grid.add_object(obj)

    def serialize(self):
        """
        Serialize the layer. The serialized layer is a dictionary with the following keys:
        ```js
        {
            // The name of the layer.
            "name": str,
            // The grid of the layer.
            "grid": JSON
        }
        ```

        Returns:
            Dict: The serialized layer.

        See Also:
            :func:`metacity.datamodel.grid.Grid.serialize` for the serialization of a grid into JSON

        Example:
            Serialize a layer:

        >>> layer = Layer("layer1", 1000.0, 1000.0)
        >>> object = metacity.io.parse('single_point_object.shp')[0]
        >>> layer.add_object(object)
        >>> layer.serialize()
        {
            "name": "layer1",
            "grid": JSON
        }

        """
        return {
            "name": self.name,
            "grid": self.grid.serialize()
        }

    @staticmethod
    def deserialize(data: Dict):
        """
        Deserialize the layer, static method.

        Args:
            data (Dict): The data to deserialize.

        Returns:
            Layer: The deserialized layer.

        See Also:
            :func:`Layer.serialize` for the serialization of a layer into a dictionary
        """

        layer = Layer(data["name"])
        layer.grid = Grid.deserialize(data["grid"])
        return layer

    @property
    def objects(self):
        """
        Generator, yields objects in the layer.

        Yields:
            Object: The objects in the layer.
        """
        for obj in self.grid.objects:
            yield obj

