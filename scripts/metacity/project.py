import shutil
import os

import numpy as np
from tqdm import tqdm

from metacity.helpers.dirtree import LayerDirectoryTree
from metacity.helpers.file import write_json, read_json
from metacity.io.cj import load_cj_file
from metacity.models.object import MetacityObject


def is_empty(objects, vertices):
    return len(vertices) == 0 or len(objects) == 0



class MetacityConfig:
    def __init__(self, dirtree: LayerDirectoryTree):
        self.shift = [0., 0., 0.]
        try:
            self.deserialize(read_json(dirtree.config))
        except:
            self.export(dirtree)


    def serialize(self):
        return {
            'shift': self.shift
        }


    def deserialize(self, data):
        self.shift = data['shift']


    def apply(self, vertices):
        vertices -= self.shift


    def update(self, vertices):
        self.shift = np.amin(vertices, axis=0).tolist()


    def export(self, dirtree: LayerDirectoryTree):
        write_json(dirtree.config, self.serialize())
            


class MetacityLayer:
    def __init__(self, name: str, project_dir: str, load_existing=True):
        self.name = name
        self.dirtree = LayerDirectoryTree(name, project_dir)
        self.dirtree.recreate_layer(load_existing)


    def update_config(self, vertices):
        config = MetacityConfig(self.dirtree)
        if self.empty:
            config.update(vertices)
        config.apply(vertices)
        config.export(self.dirtree)


    def load_cj_file(self, input_file: str):
        objects, vertices = load_cj_file(input_file)

        if is_empty(objects, vertices):
            return

        self.update_config(vertices)

        for oid, object in tqdm(objects.items()):
            mobject = MetacityObject()
            mobject.load_cityjson_object(oid, object, vertices)
            mobject.export(self.dirtree)
            

    @property
    def empty(self):
        return not self.dirtree.any_object_exists


    @property
    def objects(self):
        oids = self.dirtree.object_ids
        for oid in oids:
            obj = MetacityObject()
            obj.load(oid, self.dirtree)
            yield obj



class MetacityProject:
    def __init__(self, directory: str, load_existing=True):
        self.dir = directory
        if os.path.exists(self.dir): 
            if not load_existing:
                shutil.rmtree(self.dir)
        else:
            os.mkdir(self.dir)


    def layer(self, layer_name: str, load_existing=True):
        if layer_name in self.layers: 
            raise Exception(f'Layer {layer_name} already exists')
        
        layer = MetacityLayer(layer_name, self.dir, load_existing)
        return layer


    @property
    def layers(self):
        dirs = LayerDirectoryTree.layer_dirs(self.dir)
        return [ MetacityLayer(d, self.dir) for d in dirs ]

    

