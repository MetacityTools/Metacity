from argparse import ArgumentParser

from memory_profiler import profile

from metacity.grid.build import build_grid
from metacity.project import MetacityProject

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
    for layer in project.layers:
        grid = build_grid(layer, 200.0)
    


if __name__ == "__main__":
    main()



        