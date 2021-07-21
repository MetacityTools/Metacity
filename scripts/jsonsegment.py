#!/usr/bin/python3

import itertools
import json
import os
from argparse import ArgumentParser
from sys import path
from typing import Dict

import numpy as np
from tqdm import tqdm

from geometry.geometry import process_model
from helpers.dirtree import DirectoryTreePaths
from helpers.stats import Statistics
from models.object import MetacityObject


usage = ("Segment CityJSON file, "
         "exports segments according to LOD and geometry type"
         "into directory 'segmented'.")


def process_args():
    parser = ArgumentParser(description=usage)
    parser.add_argument('cj_input_file', type=str, help='CityJSON input file')
    parser.add_argument('-a', '--append', help='Appends processed data to existing project, if project does not exist, creates a new project', action="store_true")
    parser.add_argument('output_dir', type=str, help='Output directory, will be emptied if alreay exists')
    args = parser.parse_args()
    input_file = args.cj_input_file
    output_folder = args.output_dir
    append_action = args.append
    return input_file, output_folder, append_action


def create_output_dir_tree(output_dir, append_action):
    tree = DirectoryTreePaths(output_dir)

    if append_action:
        tree.reconstruct_existing_tree()
    else:
        tree.recreate_tree()
    return tree


def load_cj_file(input_file):
    with open(input_file, "r") as file:
        contents = json.load(file)

    objects: Dict[str, Dict] = contents["CityObjects"] 
    vertices = np.array(contents["vertices"])
    return objects, vertices


def read_config(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config


def write_config(config, config_path):
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file)


def create_config(vertices):
    shift = np.amin(vertices, axis=0)
    config = {
        'shift': shift.tolist()
    }
    return config


def apply_config(config, vertices):
    vertices -= config['shift']


def update_config(paths, vertices):
    if os.path.exists(paths.config):
        config = read_config(paths.config)
    else:
        config = create_config(vertices)
        write_config(config, paths.config)
    apply_config(config, vertices)


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


def ensure_iterable(data):
    try:
        _ = iter(data)
        return data
    except TypeError:
        return [ data ]


def get_semantics(geometry_object):
    if 'semantics' in geometry_object:
        return geometry_object['semantics']['values']
    else: 
        return None


def is_empty(objects, vertices):
    return len(vertices) == 0 or len(objects) == 0


if __name__ == "__main__":
    input_file, output_dir, append_action = process_args()
    paths = create_output_dir_tree(output_dir, append_action)
    objects, vertices = load_cj_file(input_file)
    if is_empty(objects, vertices):
        quit()

    update_config(paths, vertices)
    object_file_paths = segment_objects_into_files(paths.objects, objects)
    stats = Statistics()

    for object_file_path in tqdm(object_file_paths):
        model = MetacityObject()
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
                surface = process_model(vertices, boundries, semantics)
                model.facets.join_model(surface, lod)

            elif gtype.lower() == 'solid':
                for shell, semantics in itertools.zip_longest(boundries, ensure_iterable(semantics)):
                    surface = process_model(vertices, shell, semantics)
                    model.facets.join_model(surface, lod)

            elif gtype.lower() == 'multisolid' or gtype.lower() == 'compositesolid':
                #requires fix for multisolid semantics
                for solid, solid_semantic in itertools.zip_longest(boundries, ensure_iterable(semantics)):
                    for shell, shell_semantics in itertools.zip_longest(solid, ensure_iterable(solid_semantic)):
                        surface = process_model(vertices, shell, shell_semantics)
                        model.facets.join_model(surface, lod)

        model.consolidate()
        model.export(paths)
        
    print(stats)

        



        










