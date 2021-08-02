from argparse import ArgumentParser
from metacity.geometry.bbox import bboxes_bbox
from metacity.project import MetacityProject

from memory_profiler import profile

usage = ("Segment tiles according to optimal size")


def process_args():
    parser = ArgumentParser(description=usage)
    parser.add_argument('project_directory', type=str, help='Directory containing Metacity directory structure and model files')
    args = parser.parse_args()
    input_dir = args.project_directory
    return input_dir
 

@profile
def main():
    input_dir = process_args()
    project = MetacityProject(input_dir)
    bbox = bboxes_bbox([ layer.bbox for layer in project.layers ])
    print(bbox)    


if __name__ == "__main__":
    main()



        




    


