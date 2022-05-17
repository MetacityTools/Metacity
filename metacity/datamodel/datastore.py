from typing import Tuple
from metacity.datamodel.grid import Tile
from metacity.utils import filesystem as fs
from metacity.datamodel.layer import Layer


def layer_main_file(layer_dir: str):
    """
    Get the main file of the layer.

    Args:
        layer_dir (str): The directory path of the layer.

    Returns:
        str: Path to the main file of the layer.
    """
    return fs.join_path(layer_dir, "main.json")


def layer_layout_file(layer_dir: str):
    """
    Get the main file of the layer.

    Args:
        layer_dir (str): The directory path of the layer.

    Returns:
        str: Path to the main file of the layer.
    """
    return fs.join_path(layer_dir, "layout.json")

class DataStore:
    def __init__(self, directory):
        """
        Initialize or open an existing data store. Data store contains individual layers,
        handles storing data on the disk and loading. Internally, the data store is a 
        directory and all layers are stored in subdirectories.


        The structure of the Data Store is as follows:
        ```
        datastore_dir/
        └───layer_1/
        │   │
        │   │   BASE FILES
        │   │   ----------------------------------------------
        │   │   main.json   │ all layer data in a single file
        │   │  
        │   │   PUBLISHED FILES
        │   │   ----------------------------------------------
        │   │   layout.json │ structure of tiles for viewer
        │   │   x1_y1.json  │ tile data
        │   │   x2_y2.json  │ tile data
        │   │   ... 
        │   
        └───layer_2/
        │   ...
        ```
        
        Important files:
            * `main.json` contains all of the layer data, including object data, 
            geometry and metadata
            * `layout.json` contains the structure of the tiles for the web 
            viewer - namely tile coordinates, sizes and filenames
            * `x_y.json` contains the tile data for the tile at the specified 
            coordinates - namely the tile geometry and metadata of the objects
            with centroids contained in the tile
        Args:
            directory (str): The directory of the data store.
        """
        self.directory = directory
        #for some reason this method does not work well with temporary directories during testing
        #if not fs.is_pathname_valid(self.directory):
        #    raise ValueError(f"{self.directory} is not a valid pathname.")


    def list_layers(self):
        """
        List all layers in the data store.

        Returns:
            List[str]: The names of the layers.
        """
        return fs.list_subdirectories(self.directory)

    def get_layer(self, layer_name):
        """
        Get a layer based on its name from the data store. If the layer does not exist, 
        None is returned.

        Args:
            layer_name (str): The name of the layer to get.
        
        Returns:
            Layer: The layer.
        """
        layer_path = fs.join_path(self.directory, layer_name)
        data_file = layer_main_file(layer_path)
        if not fs.file_exists(data_file):
            return
        data = fs.read_json(data_file)
        return Layer.deserialize(data)

    @property
    def layers(self):
        """
        Generator, yields Layer stored in the data store. 

        Yields:
            Layer: each Layer in the data store.

        Example:
            Generate a list of names of layers in the data store.

        >>> ds = DataStore("store")
        >>> for name in ["terrain", "buildings", "roads"]:
        ...     ds.add_layer(Layer(name))
        >>> [l.name for l in ds.layers]
        ['terrain', 'buildings', 'roads']
        """

        for layer_name in fs.list_subdirectories(self.directory):
            layer = self.get_layer(layer_name)
            if layer is not None:
                yield layer

    def add_layer(self, layer: Layer):
        """
        Add a layer to the data store. Adding a layer to the datastore persists the 
        layer onto the disk. 

        Args:
            layer (Layer): The layer to add.

        Example:
            Add layer to existing datastore.

        >>> ds = DataStore("store")
        >>> [l.name for l in ds.layers]
        ['terrain', 'buildings']
        >>> ds.add_layer(Layer("roads"))
        >>> [l.name for l in ds.layers]
        ['terrain', 'buildings', 'roads']
        """
        
        layer_dir = self.layer_dir(layer)
        fs.create_dir_if_not_exists(layer_dir)
        fs.write_json(layer_main_file(layer_dir), layer.serialize())

    def publish_layer(self, layer: Layer):
        """
        Publish a layer to the data store. Publishing stores all of the static 
        files required by the web viewer.

        Args:
            layer (Layer): The layer to publish.

        See Also:
            :class:`DataStore` see constructor to check the layout of the
            publish files.
        """

        layer_dir = self.layer_dir(layer)
        tile_list = []
        for tile in layer.grid.tiles.values():
            tile_file = self.tile_file(layer_dir, tile)
            tile_list.append({
                "x": tile.x,
                "y": tile.y,
                "file": tile_file,
            })
            fs.write_json(tile_file, tile.serialize())

        grid_stats = {
            "tile_xdim": layer.grid.tile_xdim,
            "tile_ydim": layer.grid.tile_ydim,
            "tile_list": tile_list,
        }
        fs.write_json(layer_layout_file(layer_dir), grid_stats)


    def update_layer(self, layer: Layer):
        """
        Update a layer in the data store.

        Args:
            layer (Layer): The layer to update.
        """
        layer_dir = self.layer_dir(layer)
        fs.write_json(layer_main_file(layer_dir), layer.serialize())

    def layer_dir(self, layer: Layer):
        """
        Get the directory of the layer in the Data Store.
            
        Args:
            layer (Layer): The layer to get the directory of.
        """
        layer_dir = fs.join_path(self.directory, layer.name)
        if not fs.is_pathname_valid(layer_dir):
            raise ValueError(f"{layer_dir} is not a valid pathname.")
        return layer_dir

    def tile_file(self, layer_dir: str, tile: Tile):
        """
        Get the file path of a tile in the data store.

        Args:
            layer_dir (str): The directory of the layer.
            tile (Tuple[int, int]): The tile to get the file path of.
        
        Returns:
            str: The file path of the tile.
        """
        if not fs.is_pathname_valid(layer_dir):
            raise ValueError(f"{layer_dir} is not a valid pathname.")
        return fs.join_path(layer_dir, f"{tile.x}_{tile.y}.json")

    def __getitem__(self, layer_name: str):
        """
        Get a layer from the data store. This is a shortcut for get_layer.

        Args:
            layer_name (str): The name of the layer to get.

        Returns:
            Layer: The layer.
        """
        return self.get_layer(layer_name)
