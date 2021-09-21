from metacity.filesystem import layer as fs
from metacity.datamodel.layer.layer import MetacityLayer


class MetacityProject:
    def __init__(self, directory: str, load_existing=True):
        self.dir = directory
        fs.recrete_project(self.dir, load_existing)

    def create_layer(self, layer_name: str):
        layer_dir = fs.layer_dir(self.dir, layer_name)
        layer = MetacityLayer(layer_dir, load_existing=False)
        return layer

    def get_layer(self, layer_name: str):
        layer_dir = fs.layer_dir(self.dir, layer_name)
        layer = MetacityLayer(layer_dir)
        return layer

    def delete_layer(self, layer_name: str):
        layer_dir = fs.layer_dir(self.dir, layer_name)
        fs.base.remove_dirtree(layer_dir)

    @property
    def layer_names(self):
        return fs.layer_names(self.dir)

    @property
    def layers(self):
        names = self.layer_names
        return [self.get_layer(name) for name in names]
