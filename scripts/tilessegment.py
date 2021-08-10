from argparse import ArgumentParser
from scripts.metacity.models.object import MetacityObject
from metacity.io.stl import buffers_to_stl

from metacity.geometry.bbox import vertices_bbox
from metacity.project import MetacityLayer, MetacityProject
from metacity.models.grid import MetaRegularGrid

from memory_profiler import profile
import numpy as np
from tqdm import tqdm
from typing import Dict
usage = ("Segment tiles according to optimal size")


def process_args():
    parser = ArgumentParser(description=usage)
    parser.add_argument('project_directory', type=str, help='Directory containing Metacity directory structure and model files')
    args = parser.parse_args()
    input_dir = args.project_directory
    return input_dir


def slice_layer(layer: MetacityLayer):
    bbox = layer.bbox
    grid = MetaRegularGrid(bbox, 200.0)

    obj: MetacityObject
    for obj in tqdm(layer.objects):
        grid.insert_object(obj)


@profile
def main():
    input_dir = process_args()
    project = MetacityProject(input_dir) 
    for layer in project.layers:
        slice_layer(layer)
    


if __name__ == "__main__":
    main()



        




    


