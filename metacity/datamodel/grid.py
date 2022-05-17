import orjson
from typing import Dict, Tuple, List

from metacity.datamodel.object import Object

class Tile:
    def __init__(self, x: float, y: float, width: float, height: float):
        """
        Initialize a tile. The tile spans a rectangular area with the dimensions specified.
        Parameters x and y always define the origin coordinates and the width and height define 
        the area of the tile spanning from x to x + width, analogous for y-axis.
        
        Args:
            x (float): The base x coordinate of the tile.
            y (float): The base y coordinate of the tile.
            width (float): The width of the tile.
            height (float): The height of the tile.
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
        Serialize the tile. The serialized tile is a dictionary with the following keys:

        ```js
        {
            // The base x coordinate of the tile.
            "x": float,
            // The base y coordinate of the tile.
            "y": float,
            // The width of the tile.
            "width": float,
            // The height of the tile.
            "height": float,
            // The objects in the tile
            "objects": [ JSON, JSON, ... ]
        }
        ```

        Returns:
            Dict: The serialized tile.

        See Also:
            :func:`metacity.datamodel.object.Object.serialize` for the serialization of an Object into JSON
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
        Deserialize the tile, static method.

        Args:
            data (Dict): The data to deserialize.

        Returns:
            Tile: The deserialized tile.

        See Also:
            :func:`Tile.serialize` for the serialization of a tile into a dictionary
        """
        tile = Tile(data["x"], data["y"], data["width"], data["height"])
        tile.objects = [Object.deserialize(obj) for obj in data["objects"]]
        return tile


class Grid:
    def __init__(self, tile_xdim: float = 1000.0, tile_ydim: float = 1000.0):
        """
        Initialize a regular grid. All tiles are rectangles, aligned to axis with fixed dimensions.
        
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


    def get_tile(self, x: float, y: float):
        """
        Get the tile at the given coordinates. If the tile does not exist, it will be created.

        Args:
            x (float): The x coordinate of the pivot to get the tile for.
            y (float): The y coordinate of the pivot to get the tile for.
        """
        x = int(x / self.tile_xdim)
        y = int(y / self.tile_ydim)
        if (x, y) not in self.tiles:
            self.tiles[(x, y)] = Tile(x, y, self.tile_xdim, self.tile_ydim)
        return self.tiles[(x, y)]

    def serialize(self):
        """
        Serialize the grid. The tiles are serialized separately.
        The structure of returned data follows:

        ```js
        {
            //serialized tiles
            "tiles": [ JSON, JSON, ... ],
            //dimension of a single tile in x-axis,
            "tile_xdim": float,
            //dimension of a single tile in y-axis
            "tile_ydim": float
        }
        ```

        Returns:
            Dict: The serialized grid.

        See Also:
            :func:`Tile.serialize` for the structure of a tile JSON.
        """
        return {
            "tiles": [tile.serialize() for tile in self.tiles.values()],
            "tile_xdim": self.tile_xdim,
            "tile_ydim": self.tile_ydim
        }

    @staticmethod
    def deserialize(data: Dict):
        """
        Deserialize the grid, static method The tiles are deserialized separately.
        
        Args:
            data (Dict): The data to deserialize.

        Returns:
            Grid: The deserialized grid.
        
        See Also:
            :func:`Grid.serialize` see for the structure of the data.
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
        Iterate over all objects in the grid.

        Yields:
            Object: The objects in the grid.
        """
        for tile in self.tiles.values():
            for object in tile.objects:
                yield object