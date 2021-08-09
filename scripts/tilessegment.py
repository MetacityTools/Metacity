from argparse import ArgumentParser
from metacity.io.stl import buffers_to_stl

from metacity.geometry.bbox import vertices_bbox
from metacity.project import MetacityLayer, MetacityProject

from memory_profiler import profile
import numpy as np
from tqdm import tqdm
usage = ("Segment tiles according to optimal size")


def process_args():
    parser = ArgumentParser(description=usage)
    parser.add_argument('project_directory', type=str, help='Directory containing Metacity directory structure and model files')
    args = parser.parse_args()
    input_dir = args.project_directory
    return input_dir
 

class MetaTile:
    def __init__(self, bbox):
        self.bbox = bbox
        self.vertices = []
        self.normals = []


    def __str__(self):
        return f"{self.bbox}"


    def add_triangle(self, vertices, normal):
        self.vertices.append(vertices)
        self.normals.append(normal)

    @property
    def empty(self):
        return len(self.vertices) == 0


    def consolidate(self):
        self.vertices = np.array(self.vertices).flatten() 
        self.normals = np.array(self.normals).flatten()




def cross_point(a, b, plane, axis):
    p = (plane - b[axis]) / (a[axis] - b[axis])
    return a * p + b * (1 - p)


def one_on_plane_split(x_on_plane, y, z, plane, axis):
    mid = cross_point(y, z, plane, axis)
    y_triangle = np.array([y, mid, x_on_plane])
    z_triangle = np.array([x_on_plane, mid, z])
    return [ y_triangle, z_triangle ]


def special_case_split(triangle, plane, axis):
    a, b, c = triangle
    onplane = (triangle[:, 0] == plane)
    
    if np.count_nonzero(onplane) != 1:
        raise Exception(f"No or multiple points on plane: {onplane}.")
    
    a_onplane, b_onplane, c_onplane = onplane

    if a_onplane:
        return one_on_plane_split(a, b, c, plane, axis)

    if b_onplane:
        return one_on_plane_split(b, c, a, plane, axis)

    if c_onplane:
        return one_on_plane_split(c, a, b, plane, axis)


def roll(triangle, plane, axis):
    positioned = False
    while not positioned:
        leftplane = triangle[:, axis] < plane
        positioned = (leftplane[1] and leftplane[2]) or not (leftplane[1] or leftplane[2])
        if not positioned:
            triangle = np.roll(triangle, 1, axis=0)
    
    return triangle



def general_split(triangle, plane, axis):
    triangle = roll(triangle, plane, axis)
    a, b, c = triangle
    mid_ab = cross_point(a, b, plane, axis)
    mid_ac = cross_point(a, c, plane, axis)
    dist_ab_c = np.sum((mid_ab - c) ** 2)
    dist_b_ac = np.sum((b - mid_ac) ** 2)

    if dist_ab_c > dist_b_ac:
        return [ np.array([ a, mid_ab, mid_ac ])    , np.array([ mid_ab, b, mid_ac ]), np.array([ b, c, mid_ac ]) ]
    else:
        return [ np.array([ a, mid_ab, mid_ac ]), np.array([ mid_ab, b, c ]), np.array([ mid_ab, c, mid_ac ]) ]


def triangle_not_splitable(triangle, plane, axis):
    return np.all(triangle[:, axis] <= plane) or np.all(triangle[:, axis] >= plane)


def point_on_plane(triangle, plane, axis):
    return np.any(triangle[:, axis] == plane)


def split(triangle, plane, axis):
    if triangle_not_splitable(triangle, plane, axis):
        return [ triangle ]

    if point_on_plane(triangle, plane, axis):
        return special_case_split(triangle, plane, axis)
    else:
        return general_split(triangle, plane, axis)


def split_along_planes(triangles, planes, axis):
    tri_split = []
    for plane in planes:
        for tri in triangles:
            tri_split.extend(split(tri, plane, axis))

        triangles = tri_split
        tri_split = []
    return triangles


class MetaRegularGrid:
    def __init__(self, bbox, tile_size):
        self.bbox = bbox
        self.shift = self.bbox[0]
        self.tile_size = tile_size
        self.tiles = {}
        self.__init_grid(bbox, tile_size)


    def __init_grid(self, bbox, tile_size):
        model_range = bbox[1] - bbox[0]
        resolution = np.ceil(model_range / tile_size).astype(int)
        for x in range(resolution[0]):
            self.tiles[x] = {}
            for y in range(resolution[1]):
                self.__init_tile(bbox, x, y)


    def __init_tile(self, bbox, x, y):
        tile_base = [ self.__x_tile_base(x), self.__y_tile_base(y), bbox[0, 2] ]
        tile_top = [ self.__x_tile_top(x), self.__y_tile_top(y), bbox[1, 2] ]
        tile_bbox = np.array([tile_base, tile_top])
        self.tiles[x][y] = MetaTile(tile_bbox)


    def __x_tile_base(self, x):
        return self.shift[0] + x * self.tile_size


    def __y_tile_base(self, y):
        return self.shift[1] + y * self.tile_size


    def __x_tile_top(self, x):
        return self.shift[0] + (x + 1) * self.tile_size


    def __y_tile_top(self, y):
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
    

    def insert(self, triangle, normal):
        indices = self.vertices_tile_index(triangle)
        x_planes, y_planes = self.split_planes(indices)
        triangles = [ triangle ]

        triangles = split_along_planes(triangles, x_planes, 0)
        triangles = split_along_planes(triangles, y_planes, 1)
        
        for tri in triangles:
            x, y = self.triangle_tile_index(tri)
            self.tiles[x][y].add_triangle(tri, normal)



def slice_layer(layer: MetacityLayer):
    vertices = []
    normals = []
    
    for object in tqdm(layer.objects):
        vertices.append(object.facets.lod[2].vertices)
        normals.append(object.facets.lod[2].normals)

    vertices = np.concatenate(vertices)
    normals = np.concatenate(normals)
    vertices = vertices.reshape((vertices.shape[0] // 3, 3))
    grid = MetaRegularGrid(vertices_bbox(vertices), 200.0)
    triangles = vertices.reshape((vertices.shape[0] // 3, 3, 3))
    normals = normals.reshape((normals.shape[0] // 9, 3, 3))

    print(triangles.shape)
    for triangle, normal in tqdm(zip(triangles, normals)):
        grid.insert(triangle, normal)


    for x in grid.tiles.keys():
        for y in grid.tiles[x].keys():
            grid.tiles[x][y].consolidate()

            if not grid.tiles[x][y].empty:
                with open(f"tile_{x}_{y}.stl", "w") as stl_file:
                    buffers_to_stl(grid.tiles[x][y].vertices, grid.tiles[x][y].normals, f"tile_{x}_{y}", stl_file)

    



@profile
def main():
    input_dir = process_args()
    project = MetacityProject(input_dir) 
    for layer in project.layers:
        slice_layer(layer)
    


if __name__ == "__main__":
    main()



        




    


