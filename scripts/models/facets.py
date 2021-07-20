import numpy as np
from models.base import Model
from helpers.dirtree import DirectoryTreePaths
from geometry.multisurface import MultiSurface
import base64
import os
import json


class MultifacetedModel(Model):
    def __init__(self):
        super().__init__()
        self.vertices = self.generate_lod_dict()
        self.normals = self.generate_lod_dict()
        self.semantics = self.generate_lod_dict()


    def add_surface(self, surface: MultiSurface, lod):
        self.vertices[lod].extend(surface.vertices)
        self.normals[lod].extend(surface.normals)
        self.semantics[lod].extend(surface.semantics)


    def export_lod(self, paths: DirectoryTreePaths, lod, oid):            
        v = np.concatenate(self.vertices[lod]).flatten() 
        n = np.concatenate(self.normals[lod]).flatten()
        s = np.concatenate(self.semantics[lod]).flatten()

        data = {
            'vertices': base64.b64encode(v.astype(np.float32)).decode('utf-8'),
            'normals': base64.b64encode(n.astype(np.float32)).decode('utf-8'),
            'semantics': base64.b64encode(s.astype(np.int32)).decode('utf-8')
        }

        dir = paths.use_facet_lod_directory(lod)
        output_path = os.path.join(dir, oid + ".json")
        with open(output_path, 'w') as file:
            json.dump(data, file)