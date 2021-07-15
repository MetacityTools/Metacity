#!/usr/bin/python3

import sys
import os
import shutil
import json
from collections import defaultdict
from pprint import pprint
from typing import Dict
from tqdm import tqdm
import numpy as np
from earcut.earcut import earcut
import itertools
import matplotlib.pyplot as plt


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
vertices = np.array(contents["vertices"]) 

for oid, value in tqdm(objects.items()):
    output_path = os.path.join(objects_path, oid + ".json")
    with open(output_path, "w") as file:
        json.dump(value, file, indent=4)

present_lods = defaultdict(lambda: 0)
stats = defaultdict(lambda: 0)
present_gtypes = defaultdict(lambda: 0)



file_names = [f for f in os.listdir(objects_path) if os.path.isfile(os.path.join(objects_path, f))]



for file_name in tqdm(file_names):
    with open(os.path.join(objects_path, file_name), "r") as file:
        building = json.load(file)

        for geom in building["geometry"]:
            lod = geom["lod"]
            gtype = geom["type"]
            
            present_lods[lod] += 1
            present_gtypes[gtype] += 1

            #generate destination directory
            geometry_lod_path = os.path.join(geometry_path, str(lod))
            if not os.path.exists(geometry_lod_path):
                os.mkdir(geometry_lod_path)

            #load geometry file
            geometry_lod_file_path = os.path.join(geometry_lod_path, file_name)
            if os.path.exists(geometry_lod_file_path):
                geometry_file = open(geometry_lod_file_path, "a")
                geometries = json.load(geometry_file)
                stats["merged"] += 1 
            else:
                geometry_file = open(geometry_lod_file_path, "a")
                geometries = []
                stats["loaded"] += 1


            #process geometry
            if gtype.lower() == 'multipoint':
                pass
                #self._processPoints(geom['boundaries'], vnp, vertices)
                #gtype = pipeline.elements.MetaPoints.gtype

            elif gtype.lower() == 'multilinestring':
                pass
                #for line in geom['boundaries']:
                #    self._processLine(line, vnp, vertices)
                #gtype = pipeline.elements.MetaLines.gtype

            elif gtype.lower() == 'multisurface' or gtype.lower() == 'compositesurface':   
                for surface in geom['boundaries']:
                    
                    if len(surface) > 1:
                        face_lengths = [ len(h) for h in surface ]
                        hole_indicies = itertools.accumulate(face_lengths)
                    else:
                        hole_indicies = None
                    
                    coords = np.array(surface).flatten()

                    #fig = plt.figure()
                    #ax = fig.add_subplot(projection='3d')
                    #ax.scatter(vertices[coords][:, 0], vertices[coords][:, 1], vertices[coords][:, 2])
                    #plt.show()

                    face_vertices = vertices[coords]
                    triangle_indices = earcut(face_vertices.flatten(), hole_indicies, 3)

                    print(coords, hole_indicies, face_vertices, triangle_indices)
                    quit()
                    #TODO načítání a assembly geometrie


                #for face in geom['boundaries']:
                #    self._processFace(cj, face, vnp, vertices)
                #gtype = pipeline.elements.MetaObject.gtype

            elif gtype.lower() == 'solid':
                pass
                #for shell in geom['boundaries']:
                #    for face in shell:
                #        self._processFace(cj, face, vnp, vertices)
                #gtype = pipeline.elements.MetaObject.gtype

            elif gtype.lower() == 'multisolid' or gtype.lower() == 'compositesolid':
                pass
                #for solid in geom['boundaries']:
                #    for shell in solid:
                #        for face in shell:
                #            self._processFace(cj, face, vnp, vertices)



            geometries.append(geom)

            #save merged geometries
            json.dump(geometries, geometry_file)



print(present_lods)
print(stats)
print(present_gtypes)
        



        










