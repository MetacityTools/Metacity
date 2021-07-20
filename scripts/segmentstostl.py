import os
from helpers.file import id_from_filename
from argparse import ArgumentParser
import numpy as np
import base64
import json
from geometry.export import buffers_to_stl
from tqdm import tqdm
from helpers.dirtree import DirectoryTreePaths


usage = ("Convert selected segments into STL file")

parser = ArgumentParser(description=usage)
parser.add_argument('input_directory', type=str, help='Directory containing Metacity directory structure and model files')


def process_args():
    args = parser.parse_args()
    input_dir = args.input_directory
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


input_dir = process_args()
paths = DirectoryTreePaths(input_dir)
paths.recreate_stl()
lod_dirs = paths.lod_dirs


for lod in lod_dirs:
    lod_dir = os.path.join(paths.geometry, lod)
    file_list = []
    for object_file in tqdm(os.listdir(lod_dir)):
        absolute_object_file = os.path.join(lod_dir, object_file)
        if os.path.isfile(absolute_object_file):
            file_list.append(absolute_object_file)


    stl_output = lod_dir_to_output_file_name(lod) + '.stl'
    abs_stl_output = os.path.join(paths.stl, stl_output) 
    
    
    with open(abs_stl_output, 'w') as stl_file:
        for object_file in tqdm(file_list):
            with open(object_file, 'r') as file:
                contents = json.load(file)

            vertices = base64_to_float32(contents['vertices'])
            normals = base64_to_float32(contents['normals'])
            semantics = base64_to_int32(contents['semantics'])

            object_id = id_from_filename(object_file)
            buffers_to_stl(vertices, normals, object_id, stl_file)


























