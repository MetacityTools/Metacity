#!/usr/bin/python3

import itertools
import sys
import os
import json
from typing import Dict
from tqdm import tqdm
import numpy as np
from helpers.dirtree import DirectoryTreePaths
from helpers.stats import Statistics
from models.model import MetacityModel
from geometry.geometry import process_multisurface
from argparse import ArgumentParser



usage = ("Segment CityJSON file, "
         "exports segments according to LOD and geometry type"
         "into directory 'segmented'.")

parser = ArgumentParser(description=usage)
parser.add_argument('cj_input_file', type=str, help='CityJSON input file')


def generate_output_dir(input_file):
    input_dir = os.path.dirname(input_file)
    return os.path.join(input_dir, "segmented")


def process_args():
    args = parser.parse_args()
    input_arg = args.cj_input_file
    input_file = os.path.join(os.getcwd(), input_arg)
    output_folder = generate_output_dir(input_file) #sys.argv[2]
    return input_file, output_folder


def create_output_dir_tree(output_dir):
    tree = DirectoryTreePaths(output_dir)
    tree.recreate_tree()
    return tree


def load_cj_file(input_file):
    with open(input_file, "r") as file:
        contents = json.load(file)

    objects: Dict[str, Dict] = contents["CityObjects"] 
    vertices = np.array(contents["vertices"])
    return objects, vertices


def segment_objects_into_files(objects_path, objects):
    object_file_paths = []
    for oid, value in tqdm(objects.items()):
        output_path = os.path.join(objects_path, oid + ".json")
        with open(output_path, "w") as file:
            json.dump(value, file, indent=4)
        object_file_paths.append(output_path)
    return object_file_paths


def get_geometry_stats(geometry_object):
    lod = geometry_object["lod"]
    gtype = geometry_object["type"].lower()
    return lod, gtype


def generate_semantic_null():
    return [ None ]


def get_semantics(geometry_object):
    if 'semantics' in geometry_object:
        return geometry_object['semantics']['values']
    else: 
        return generate_semantic_null()




input_file, output_dir = process_args()
paths = create_output_dir_tree(output_dir)
objects, vertices = load_cj_file(input_file) 
object_file_paths = segment_objects_into_files(paths.objects, objects)
stats = Statistics()

for object_file_path in tqdm(object_file_paths):
    model = MetacityModel()
    model.load_cityjson_object(object_file_path)

    for geometry_object in model.geometry:
        lod, gtype = get_geometry_stats(geometry_object)
        stats.parsed_geometry(lod, gtype)
        semantics = get_semantics(geometry_object)
        boundries = geometry_object['boundaries']

        #process geometry
        if gtype.lower() == 'multipoint':
            pass
            #self._processPoints(geom['boundaries'], vnp, vertices)

        elif gtype.lower() == 'multilinestring':
            pass
            #for line in geom['boundaries']:
            #    self._processLine(line, vnp, vertices)

        elif gtype.lower() == 'multisurface' or gtype.lower() == 'compositesurface':   
            surface = process_multisurface(vertices, boundries, semantics)
            model.facets.add_surface(surface, lod)

        elif gtype.lower() == 'solid':
            for shell, semantics in itertools.zip_longest(boundries, semantics):
                surface = process_multisurface(vertices, shell, semantics)
                model.facets.add_surface(surface, lod)

        elif gtype.lower() == 'multisolid' or gtype.lower() == 'compositesolid':
            for solid in boundries:
                for shell in solid:
                    surface = process_multisurface(vertices, boundries, semantics)
                    model.facets.add_surface(surface, lod)

    model.export(paths)



print(stats)

        



        










