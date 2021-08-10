from typing import Dict

import os
import numpy as np
from metacity.geometry.splitting import split_along_planes
from metacity.models.object import MetacityObject
from metacity.models.model import FacetModel, LineModel, PointModel, TileModel
from metacity.helpers.dirtree import LayerDirectoryTree
from metacity.helpers.file import write_json, read_json


class MetaGirdConfig:
    def __init__(self, dirtree: LayerDirectoryTree):
        self.oid_to_id = {}
        self.id_to_oid = {}
        self.id_counter = 0
        try:
            self.deserialize(read_json(dirtree.grid))
        except:
            self.export(dirtree.grid)


    def id_for_oid(self, oid):
        if oid not in self.oid_to_id:
           self.oid_to_id[oid] = self.id_counter
           self.id_to_oid[self.id_counter] = oid
           self.id_counter += 1 
        return self.oid_to_id[oid]
 

    def serialize(self):
            return {
                'oid_to_id': self.oid_to_id,
                'id_to_oid': self.id_to_oid,
                'id_counter': self.id_counter
            }


    def deserialize(self, data):
        self.oid_to_id = data['oid_to_id']
        self.id_to_oid = data['id_to_oid']
        self.id_counter = data['id_counter']


    def export(self, dirtree: LayerDirectoryTree):
        write_json(dirtree.config, self.serialize())




class MetaTileLods:
    def __init__(self, primitive):
        self.lod = { i: TileModel(primitive) for i in range(0, 5) }



class MetaTile:
    def __init__(self, bbox, x, y):
        self.bbox = bbox

        self.x = x
        self.y = y

        self.points = MetaTileLods(PointModel)
        self.lines = MetaTileLods(LineModel)
        self.facets = MetaTileLods(FacetModel)


    @property
    def empty(self):
        return len(self.vertices) == 0


