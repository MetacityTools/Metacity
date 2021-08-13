import numpy as np
from metacity.geometry.splitting import split_along_planes
from metacity.grid.config import RegularGridConfig
from metacity.models.model import FacetModel
from metacity.models.object import MetacityObject


class RegularGridSlicer:
    def __init__(self, config: RegularGridConfig):
        self.config = config


    def split_planes(self: RegularGridConfig, indices):
        min_box = np.amin(indices, axis=0)
        max_box = np.amax(indices, axis=0)

        x_planes = []
        for x in range(min_box[0], max_box[0]):
            x_planes.append(self.config.x_tile_top(x))

        y_planes = []
        for y in range(min_box[1], max_box[1]):
            y_planes.append(self.config.y_tile_top(y))

        return x_planes, y_planes


    def vertices_tile_index(self, vertices):
        return np.floor(((vertices - self.config.shift) / self.config.tile_size)[:, 0:2]).astype(int)


    def split_triangle(self, triangle):
        indices = self.vertices_tile_index(triangle)
        x_planes, y_planes = self.split_planes(indices)
        triangles = [ triangle ]
        triangles = split_along_planes(triangles, x_planes, 0)
        triangles = split_along_planes(triangles, y_planes, 1)
        return triangles


    def slice_facet_model(self, model: FacetModel):
        sliced_model = FacetModel()
        sliced_model.semantics_meta = model.semantics_meta
        for triangle, normals, semantics in model.items:
            triangles = self.split_triangle(triangle)
            sliced_model.extend(triangles, normals, semantics)
        return sliced_model


    def slice_facet_models(self, object: MetacityObject):
        for lod in range(0, 5):
            model = object.facets.lod[lod]
            if model.exists:
                #DANGER ZONE, modyfing the metacity raw object for data transfer purpouses, shoud not be exported now
                model = self.slice_facet_model(model)
                object.facets.lod[lod] = model


    def slice_object(self, object: MetacityObject):
        self.slice_facet_models(object)
        #TODO lines + points

        