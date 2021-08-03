from argparse import ArgumentParser

from numpy.lib.shape_base import tile
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
                self.__init_tile(bbox, tile_size, x, y)


    def __init_tile(self, bbox, tile_size, x, y):
        tile_base = [ self.shift[0] + x * tile_size, self.shift[1] + y * tile_size, bbox[0, 2] ]
        tile_top = [ self.shift[0] + (x + 1) * tile_size, self.shift[1] + (y + 1) * tile_size, bbox[1, 2] ]
        tile_bbox = np.array([tile_base, tile_top])
        self.tiles[x][y] = MetaTile(tile_bbox)


    def triangle_tile_index(self, triangle):
        return np.floor(((triangle - self.shift) / self.tile_size)[:, 0:2]).astype(int)
                

    def insert(self, triangle):
        indices = self.triangle_tile_index(triangle)
        
        if np.array_equal(indices[0], indices[1]) and np.array_equal(indices[0], indices[2]):
            pass
            #all equal
        else:
            print(triangle)
            print(indices)
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



        




    


