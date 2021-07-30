import os
from argparse import ArgumentParser
from metacity.io.stl import export_objects_stl
from metacity.project import MetacityProject

from memory_profiler import profile

usage = ("Convert selected segments into STL file")



def process_args():
    parser = ArgumentParser(description=usage)
    parser.add_argument('project_directory', type=str, help='Directory containing Metacity directory structure and model files')
    args = parser.parse_args()
    input_dir = args.project_directory
    return input_dir


def lod_dir_to_output_file_name(lod_dir):
    joiner = '_'
    return joiner.join(os.path.split(lod_dir)) + '.stl'


@profile
def main():
    input_dir = process_args()
    project = MetacityProject(input_dir)

    lod1 = open("lod1.stl", 'w')
    lod2 = open("lod2.stl", 'w')
    
    for layer in project.layers:
        export_objects_stl([lod1, lod2], layer.objects, [1, 2])

    lod1.close()
    lod2.close()


if __name__ == "__main__":
    main()



















