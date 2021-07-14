#!/usr/bin/python3

import sys
import os
import shutil
import json
from pprint import pprint
from typing import Dict
from tqdm import tqdm

usage = ("Segment CityJSON into tiles,"
         "exports the tiles as smaller CJ files"
         "into directory 'segmented'."
         "jsonsegment.py [input file]")


def readable(file):
    print(file)
    f = open(file, "r")
    return f.readable()


def writable(file):
    f = open(file, "w")
    return f.writable()


def generate_output_dir(input_file):
    input_dir = os.path.dirname(input_file)
    return os.path.join(input_dir, "segmented")


def process_args():
    input_arg = sys.argv[1]
    input_file = os.path.join(os.getcwd(), input_arg)
    output_folder = generate_output_dir(input_file) #sys.argv[2]
    return input_file, output_folder


def parse_args():
    if len(sys.argv) < 2:
        print(usage)
        return None, None
    else:
        return process_args()




input_file, output_dir = parse_args()
print(input_file, output_dir)


if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

os.mkdir(output_dir)
objects_path = os.path.join(output_dir, "objects")
os.mkdir(objects_path)
geometry_path = os.path.join(output_dir, "geometry")
os.mkdir(geometry_path)

with open(input_file, "r") as file:
    contents = json.load(file)

objects: Dict[str, Dict] = contents["CityObjects"] 

for oid, value in tqdm(objects.items()):
    output_path = os.path.join(objects_path, oid + ".json")
    with open(output_path, "w") as file:
        json.dump(value, file, indent=4)

present_lods = {}
file_names = [f for f in os.listdir(objects_path) if os.path.isfile(os.path.join(objects_path, f))]


for file_name in file_names:
    with open(os.path.join(objects_path, file_name), "r") as file:
        building = json.load(file)

        for geom in building["geometry"]:
            lod = geom["lod"]
            if lod in present_lods:
                present_lods[lod] += 1
            else :
                present_lods[lod] = 1

#TODO 
#pomoci earcut vytriangulovat geometrii

        



        










