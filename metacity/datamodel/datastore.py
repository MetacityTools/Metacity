from metacity.utils import filesystem as fs
from metacity.datamodel.layer import Layer


def layer_main_file(layer_dir):
    """
    Get the main file of the layer.

    Args:
        layer_dir (str): The directory path of the layer.

    Returns:
        str: Path to the main file of the layer.
    """
    return fs.join_path(layer_dir, "main.json")


class DataStore:
    def __init__(self, directory):
        """
        Initialize or open an existing data store. Data store contains individual layers,
        handles storing data on the disk and loading. Internally, the data store is a 
        directory and all layers are stored in subdirectories.
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
        Add a layer to the data store.

        Args:
            layer (Layer): The layer to add.
        """
        layer_dir = self.layer_dir(layer)
        fs.create_dir_if_not_exists(layer_dir)
        fs.write_json(layer_main_file(layer_dir), layer.serialize())

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

    def __getitem__(self, layer_name: str):
        """
        Get a layer from the data store. This is a shortcut for get_layer.

        Args:
            layer_name (str): The name of the layer to get.

        Returns:
            Layer: The layer.
        """
        return self.get_layer(layer_name)

