from argparse import ArgumentParser

from metacity.geometry.bbox import vertices_bbox
from metacity.project import MetacityLayer, MetacityProject

from memory_profiler import profile
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from pprint import pprint
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

        
    def __str__(self):
        return f"{self.bbox}"



def special_case_two_on_plane(z, plane, triangle):
    if z > plane:
        return [], [ triangle ]
    else: 
        return [ triangle ], []


def special_case_one_on_plane_split(y, z, plane, triangle, on_plane_idx, y_idx, z_idx):
    p = (plane - z) / (y - z)
    mid = triangle[y_idx] * p + triangle[z_idx] * (1 - p)
    y_triangle = np.array([triangle[y_idx], mid, triangle[on_plane_idx]])
    z_triangle = np.array([triangle[on_plane_idx], mid, triangle[z_idx]])
    if y < plane and z > plane:
        return y_triangle, z_triangle
    else:
        return z_triangle, y_triangle


def special_case_one_on_plane(y, z, plane, triangle, on_plane_idx, y_idx, z_idx):
    if y > plane and z > plane:
        return [], [ triangle ]
    elif y < plane and z < plane:
        return [ triangle ], []
    else:
        return special_case_one_on_plane_split(y, z, plane, triangle, on_plane_idx, y_idx, z_idx)


def handle_special_cases(triangle, plane, axis):
    a, b, c = triangle
    a_onplane, b_onplane, c_onplane = (triangle[:, 0] == plane)

    if a_onplane and b_onplane and c_onplane:
        return [ triangle ], []

    if a_onplane and b_onplane:
        return special_case_two_on_plane(c[axis], plane, triangle)
    
    if b_onplane and c_onplane:
        return special_case_two_on_plane(a[axis], plane, triangle)
    
    if c_onplane and a_onplane:
        return special_case_two_on_plane(b[axis], plane, triangle)

    if a_onplane:
        return special_case_one_on_plane(b[axis], c[axis], plane, triangle, 0, 1, 2)

    if b_onplane:
        return special_case_one_on_plane(c[axis], a[axis], plane, triangle, 1, 2, 0)

    if c_onplane:
        return special_case_one_on_plane(a[axis], b[axis], plane, triangle, 2, 0, 1)


def x_split_triangle(triangle, plane):
    onplane = (triangle[:, 0] == plane)

    if np.any(onplane):
        return handle_special_cases(triangle, plane, 0)

    #TODO


def x_split(triangles, planes):
    planes.sort()
    segmented = []

    for plane in planes:
        for triangle in triangles:
            x_split_triangle(triangle, plane)



    #TODO


class MetaRegularGrid:
    def __init__(self, bbox, tile_size):
        self.bbox = bbox
        self.shift = self.bbox[0]
        self.tile_size = tile_size
        #self.epsilon = tile_size * 0.0001 # test this value TBA
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




    def triangle_tile_index(self, triangle):
        return np.floor(((triangle - self.shift) / self.tile_size)[:, 0:2]).astype(int)


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
                
                

    def insert(self, triangle):
        indices = self.triangle_tile_index(triangle)

        if np.array_equal(indices[0], indices[1]) and np.array_equal(indices[0], indices[2]):
            pass
            #all equal, not neccasary to slice
        else:
            print(indices)
            x_planes, y_planes = self.split_planes(indices)
            print(x_planes, y_planes)

            triangles = [ triangle ]
            print(triangles)
            triangles = x_split(triangles, x_planes)
            quit()






def slice_layer(layer: MetacityLayer):
    vertices = []
    
    for object in tqdm(layer.objects):
        vertices.append(object.facets.lod[2].vertices)

    vertices = np.concatenate(vertices)
    vertices = vertices.reshape((vertices.shape[0] // 3, 3))
    grid = MetaRegularGrid(vertices_bbox(vertices), 100.0)
    triangles = vertices.reshape((vertices.shape[0] // 3, 3, 3))

    for triangle in triangles:
        grid.insert(triangle)







    #plt.scatter(vertices[:, 0], vertices[:, 1])
    #plt.show()




@profile
def main():
    input_dir = process_args()
    project = MetacityProject(input_dir) 
    for layer in project.layers:
        slice_layer(layer)
    


if __name__ == "__main__":
    main()



        




    


