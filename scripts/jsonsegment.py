#!/usr/bin/python3

import itertools
import json
import os
from argparse import ArgumentParser
from typing import Dict

import numpy as np
from tqdm import tqdm

from geometry.geometry import process_multisurface
from helpers.dirtree import DirectoryTreePaths
from helpers.stats import Statistics
from models.model import MetacityModel


usage = ("Segment CityJSON file, "
         "exports segments according to LOD and geometry type"
         "into directory 'segmented'.")



def process_args():
    parser = ArgumentParser(description=usage)
    parser.add_argument('cj_input_file', type=str, help='CityJSON input file')
    parser.add_argument('output_dir', type=str, help='Output directory, will be emptied if alreay exists')
    args = parser.parse_args()
    input_file = args.cj_input_file
    output_folder = args.output_folder
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

    shift = np.amin(vertices, axis=0)
    vertices = vertices - shift
    return objects, vertices, shift.tolist()


def create_config(paths, shift):
    config = {
        'shift': shift
    }

    config_path = os.path.join(paths.output, 'config.json')
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file)


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



if __name__ == "__main__":
    input_file, output_dir = process_args()
    paths = create_output_dir_tree(output_dir)
    objects, vertices, shift = load_cj_file(input_file)
    create_config(paths, shift)
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
                pass
                #requires fix for multisolid semantics
                #for solid in boundries:
                #    for shell, semantics in itertools.zip_longest(boundries, semantics):
                #        surface = process_multisurface(vertices, shell, semantics)
                #        model.facets.add_surface(surface, lod)

        model.export(paths)
        
    print(stats)

        



        










