from metacity.datamodel.object import Object
from metacity.datamodel.grid import Grid
from typing import List, Dict

class Layer:
    def __init__(self, name, tile_xdim = 1000.0, tile_ydim= 1000.0):
        """
        Initialize a layer. Layer represents a collection of objects.
        
        Args:
            name (str): The name of the layer.
            tile_xdim (float): The x dimension of the tiles. Default is 1000.0.
            tile_ydim (float): The y dimension of the tiles. Default is 1000.0.
        """
        self.name = name
        self.grid = Grid(tile_xdim, tile_ydim)
    
    def add_object(self, obj: Object):
        """
        Add an object to the layer.
        
        Args:
            obj (Object): The object to add.
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
        Serialize the layer.

        Returns:
            Dict: The serialized layer.
        """
        return {
            "name": self.name,
            "grid": self.grid.serialize()
        }

    @staticmethod
    def deserialize(data: Dict):
        """
        Deserialize the layer.

        Args:
            data (Dict): The data to deserialize.
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

