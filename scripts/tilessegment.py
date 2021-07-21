from argparse import ArgumentParser

from helpers.dirtree import DirectoryTreePaths

usage = ("Segment tiles according to optimal size")


def process_args():
    parser = ArgumentParser(description=usage)
    parser.add_argument('project_directory', type=str, help='Directory containing Metacity directory structure and model files')
    args = parser.parse_args()
    input_dir = args.project_directory
    return input_dir
 

if __name__ == "__main__":
    input_dir = process_args()
    paths = DirectoryTreePaths(input_dir)
    for lod in paths.facet_lods:
        models = paths.paths_to_models(lod)
        #WIP SEGMENT NEBO NECO



        




    


