from metacity.dirtree import layer as tree
from metacity.datamodel.layer.layer import MetacityLayer


class MetacityProject:
    def __init__(self, directory: str, load_existing=True):
        self.dir = directory
        tree.recrete_project(self.dir, load_existing)


    def layer(self, layer_name: str, load_existing=True):  
        layer_dir = tree.layer_dir(self.dir, layer_name)   
        layer = MetacityLayer(layer_dir, load_existing)
        return layer


    @property
    def layer_names(self):
        return tree.layer_names(self.dir)


    @property
    def layers(self):
        names = self.layer_names
        return [ self.layer(name) for name in names ]