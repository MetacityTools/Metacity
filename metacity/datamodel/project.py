from metacity.filesystem import layer as fs
from metacity.filesystem import file as fsf
from metacity.datamodel.layer import Layer, LayerOverlay


class Project:
    def __init__(self, directory: str):
        self.dir = directory
        fs.create_project(self.dir)

    def create_layer(self, layer_name: str):
        layer_dir = fs.non_coliding_layer_dir(self.dir, layer_name)
        layer = Layer(layer_dir)
        return layer

    def create_overlay(self, layer_name: str):
        layer_dir = fs.non_coliding_layer_dir(self.dir, layer_name)
        layer = LayerOverlay(layer_dir)
        return layer

    def get_layer(self, layer_name: str):
        layer_dir = fs.layer_dir(self.dir, layer_name)
        layer = Layer(layer_dir)
        return layer

    def get_overlay(self, layer_name: str):
        layer_dir = fs.layer_dir(self.dir, layer_name)
        layer = LayerOverlay(layer_dir)
        return layer

    def delete_layer(self, layer_name: str):
        layer_dir = fs.layer_dir(self.dir, layer_name)
        fs.base.remove_dirtree(layer_dir)

    def delete_overlay(self, layer_name: str):
        self.delete_layer(layer_name)

    def build_layout(self):
        layout = []
        for layer in self.layers:
            layout.append(layer.build_layout())
        fsf.write_json(fs.base.project_layout(self.dir), layout)

    def get_layout(self):
        file = fs.base.project_layout(self.dir)
        if fs.base.file_exists(file):
            return fsf.read_json(file)
        return []

    @property
    def layer_names(self):
        return fs.layer_names(self.dir)

    @property
    def layers(self):
        names = self.layer_names
        return [self.get_layer(name) for name in names]
