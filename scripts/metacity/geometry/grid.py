from metacity.project import MetacityLayer
from typing import Dict

from metacity.geometry.splitting import split_along_planes
from metacity.models.grid import MetaTile
from metacity.models.model import FacetModel
import numpy as np




class RegularGridBuilder:
    def __init__(self, bbox, tile_size):
        self.bbox = bbox
        self.shift = self.bbox[0]
        self.tile_size = tile_size
        self.tiles: Dict[str, Dict[str, MetaTile]] = {}
        self.init_grid()


    def init_tile(self, x, y):
        tile_base = [ self.x_tile_base(x), self.y_tile_base(y), self.bbox[0, 2] ]
        tile_top = [ self.x_tile_top(x), self.y_tile_top(y), self.bbox[1, 2] ]
        tile_bbox = np.array([tile_base, tile_top])
        self.tiles[x][y] = MetaTile(tile_bbox)


    def init_grid(self):
        model_range = self.bbox[1] - self.bbox[0]
        resolution = np.ceil(model_range / self.tile_size).astype(int)
        for x in range(resolution[0]):
            self.tiles[x] = {}
            for y in range(resolution[1]):
                self.init_tile(self, x, y)


    def x_tile_base(self, x):
        return self.shift[0] + x * self.tile_size


    def y_tile_base(self, y):
        return self.shift[1] + y * self.tile_size


    def x_tile_top(self, x):
        return self.shift[0] + (x + 1) * self.tile_size


    def y_tile_top(self, y):
        return self.shift[1] + (y + 1) * self.tile_size


    def vertices_tile_index(self, vertices):
        return np.floor(((vertices - self.shift) / self.tile_size)[:, 0:2]).astype(int)


    def triangle_tile_index(self, triangle):
        center = np.sum(triangle, axis=0) / 3
        return np.floor(((center - self.shift) / self.tile_size)[0:2]).astype(int)


    def split_planes(self, indices):
        min_box = np.amin(indices, axis=0)
        max_box = np.amax(indices, axis=0)

        x_planes = []
        for x in range(min_box[0], max_box[0]):
            x_planes.append(self.__x_tile_top(x))

        y_planes = []
        for y in range(min_box[1], max_box[1]):
            y_planes.append(self.__y_tile_top(y))

        return x_planes, y_planes





def insert_triangle(grid: RegularGridBuilder, oid, lod, triangle, normals, semantics):
    ## TODO refactor

    indices = grid.vertices_tile_index(triangle)
    x_planes, y_planes = grid.split_planes(indices)
    triangles = [ triangle ]

    triangles = split_along_planes(triangles, x_planes, 0)
    triangles = split_along_planes(triangles, y_planes, 1)
    

    ##TODO here
    bid = config.id_for_oid(oid)

    for tri in triangles:
        x, y = grid.triangle_tile_index(tri)
        model = FacetModel()
        model.vertices = tri.flatten()
        model.normals = normals.flatten()
        model.semantics = semantics.flatten()
        grid.tiles[x][y].add_facet_model(bid, lod, model)



def insert_object(grid, object):
    for lod in range(0, 5):
        if object.facets.lod[lod].exists:
            for triangle, normals, semantics in object.facets.lod[lod].items:
                insert_triangle(grid, object.oid, lod, triangle, normals, semantics)



def build_grid(layer: MetacityLayer, tile_size):
    grid = RegularGridBuilder(layer.bbox, tile_size)

    for obj in layer.objects:
        insert_object(grid, obj)



