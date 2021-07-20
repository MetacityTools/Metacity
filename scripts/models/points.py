import numpy as np
from models.base import Model
from helpers.dirtree import DirectoryTreePaths
import base64
import os
import json


class PointModel(Model):
    def __init__(self):
        self.vertices = self.generate_lod_dict()
        self.semantics = self.generate_lod_dict()


    def add_point(self, point):
        pass
        #self.vertices[lod].append(point.vertices)
        #self.semantics[lod].append(point.semantics)


    def export_lod(self, paths: DirectoryTreePaths, lod, oid):            
        v = np.concatenate(self.vertices[lod]).flatten() 
        s = np.concatenate(self.semantics[lod]).flatten()

        data = {
            'vertices': base64.b64encode(v.astype(np.float32)).decode('utf-8'),
            'semantics': base64.b64encode(s.astype(np.int32)).decode('utf-8')
        }

        dir = paths.use_points_lod_directory(lod)
        output_path = os.path.join(dir, oid + ".json")
        with open(output_path, 'w') as file:
            json.dump(data, file)
