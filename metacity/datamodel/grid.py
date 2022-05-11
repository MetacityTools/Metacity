import orjson
from typing import Dict, Tuple, List

from metacity.datamodel.object import Object

class Tile:
    def __init__(self, x, y, width, height):
        """
        Initialize a tile.
        
        Args:
            x (int): The x coordinate of the tile.
            y (int): The y coordinate of the tile.
            width (int): The width of the tile.
            height (int): The height of the tile.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.objects: List[Object] = []

    def add_object(self, object: Object):
        """
        Add an object to the tile. 
        
        Args:
            object (Object): The object to add.
        """
        self.objects.append(object)

    def serialize(self):
        """
        Serialize the tile. 

        Returns:
            Dict: The serialized tile.
        """
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "objects": [obj.serialize() for obj in self.objects]
        }

    @staticmethod
    def deserialize(data: Dict):
        """
        Deserialize the tile.

        Args:
            data (Dict): The data to deserialize.
        """
        tile = Tile(data["x"], data["y"], data["width"], data["height"])
        tile.objects = [Object.deserialize(obj) for obj in data["objects"]]
        return tile


class Grid:
    def __init__(self, tile_xdim=1000.0, tile_ydim=1000.0):
        """
        Initialize a regular grid. All tiles are AABBs, aligned to zero coordinates with fixed dimensions.
        
        Args:
            tile_xdim (float): The x dimension of a single tile. Default is 1000.0.
            tile_ydim (float): The y dimension of a single tile. Default is 1000.0.
        """
        self.tiles: Dict[Tuple[int, int], Tile] = {}
        self.tile_xdim = tile_xdim
        self.tile_ydim = tile_ydim

    def add_object(self, object: Object):
        """
        Add an object to the grid. The object will be added to the tile it is contained in.
        If object has multiple geometries, take average of all geometry centroids and 
        use it as the tile selection pivot.

        Args:
            object (Object): The object to add.
        """

        pivot = [0, 0]

        for geometry in object.geometry:
            c = geometry.centroid
            pivot[0] += c[0]
            pivot[1] += c[1]
        
        pivot[0] /= len(object.geometry)
        pivot[1] /= len(object.geometry)

        tile = self.get_tile(pivot[0], pivot[1])
        tile.add_object(object)


    def get_tile(self, x, y):
        """
        Get the tile at the given coordinates. If the tile does not exist, it will be created.

        Args:
            x (int): The x coordinate of the pivot to get the tile for.
            y (int): The y coordinate of the pivot to get the tile for.
        """
        x = int(x / self.tile_xdim)
        y = int(y / self.tile_ydim)
        if (x, y) not in self.tiles:
            self.tiles[(x, y)] = Tile(x, y, self.tile_xdim, self.tile_ydim)
        return self.tiles[(x, y)]

    def serialize(self):
        """
        Serialize the grid. The tiles are serialized separately.

        Returns:
            Dict: The serialized grid.
        """
        return {
            "tiles": [tile.serialize() for tile in self.tiles.values()],
            "tile_xdim": self.tile_xdim,
            "tile_ydim": self.tile_ydim
        }

    @staticmethod
    def deserialize(data: Dict):
        """
        Deserialize the grid. The tiles are deserialized separately.
        
        Args:
            data (Dict): The data to deserialize.
        """
        grid = Grid()
        grid.tile_xdim = data["tile_xdim"]
        grid.tile_ydim = data["tile_ydim"]
        for tile in data["tiles"]:
            x = tile["x"]
            y = tile["y"]
            grid.tiles[(x, y)] = Tile.deserialize(tile)
        return grid

    @property
    def objects(self):
        """
        Get all objects in the grid.

        Yields:
            Object: The objects in the grid.
        """
        for tile in self.tiles.values():
            for object in tile.objects:
                yield object