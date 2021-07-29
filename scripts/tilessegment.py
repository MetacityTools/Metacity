from argparse import ArgumentParser
from json import load
import os
from metacity.helpers.dirtree import DirectoryTree
from metacity.io.core import load_models

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
    paths = DirectoryTree(input_dir)
    paths.recreate_tiles()
    for lod in paths.facet_lods:
        model_paths = paths.models_for_lods(lod)
        output_dir = os.path.join(paths.tiles, lod)
        paths.use_directory(output_dir)

        models = load_models(model_paths)
        
        

        print(len(models))


if __name__ == "__main__":
    main()



        




    


