import base64
import json
import os
from argparse import ArgumentParser

import numpy as np
from tqdm import tqdm

from geometry.export import buffers_to_stl
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
    return joiner.join(os.path.split(lod_dir)) 


def base64_to_type(b64data, type):
    bdata = base64.b64decode(b64data)
    data = np.frombuffer(bdata, dtype=type)
    return data


def base64_to_float32(b64data):
    return base64_to_type(b64data, np.float32)


def base64_to_int32(b64data):
    return base64_to_type(b64data, np.int32)


if __name__ == "__main__":
    input_dir = process_args()
    paths = DirectoryTreePaths(input_dir)
    paths.recreate_stl()

    for lod in paths.primitive_type_lod_dirs:
        models = paths.paths_to_models(lod)
        stl_output = lod_dir_to_output_file_name(lod) + '.stl'
        abs_stl_output = os.path.join(paths.stl, stl_output) 

        with open(abs_stl_output, 'w') as stl_file:
            for object_file in tqdm(models):
                with open(object_file, 'r') as file:
                    contents = json.load(file)

                vertices = base64_to_float32(contents['vertices'])
                normals = base64_to_float32(contents['normals'])
                semantics = base64_to_int32(contents['semantics'])

                object_id = id_from_filename(object_file)
                buffers_to_stl(vertices, normals, object_id, stl_file)


























