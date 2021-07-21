import os
from argparse import ArgumentParser

from tqdm import tqdm

from geometry.io import buffers_to_stl, load_model
from helpers.dirtree import DirectoryTreePaths
from helpers.file import id_from_filename

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


if __name__ == "__main__":
    input_dir = process_args()
    paths = DirectoryTreePaths(input_dir)
    paths.recreate_stl()

    for lod in paths.primitive_lods:
        models = paths.models_for_lods(lod)
        stl_output = lod_dir_to_output_file_name(lod)
        abs_stl_output = os.path.join(paths.stl, stl_output) 

        with open(abs_stl_output, 'w') as stl_file:
            for object_file in tqdm(models):
                with open(object_file, 'r') as file:
                    model = load_model(file)
                object_id = id_from_filename(object_file)
                buffers_to_stl(model.vertices, model.normals, object_id, stl_file)


























