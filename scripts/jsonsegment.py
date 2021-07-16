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
from earcut.earcut import earcut, normal
import itertools
import matplotlib.pyplot as plt
import base64



def buffers_to_stl(flat_vertices, flat_normals, filename):
    with open(filename, "w") as file:
        file.write("solid model\n")

        verts = flat_vertices.reshape((flat_vertices.shape[0] // 9, 3, 3))
        norms = flat_normals.reshape((flat_normals.shape[0] // 9, 3, 3))

        #center = np.average(np.average(verts, axis=1), axis=0)
        #verts = verts - center

        for tri_vertex, tri_normal in zip(verts, norms):
            file.write(f"    facet normal ")
            for i in range(3):
                file.write(str(tri_normal[0][i]))
                file.write(" ")
            file.write("\n")

            file.write(f"       outer loop\n")
            for i in range(3):
                file.write(f"          vertex {tri_vertex[i][0]} {tri_vertex[i][1]} {tri_vertex[i][2]}\n")            
            file.write(f"       endloop\n")
            file.write(f"    endfacet\n")

        file.write("solid model\n")





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



def process_building_geometry(geometry_path, file, vertices, present_lods, stats, present_gtypes, file_name):
    building = json.load(file)
    export_vertices = []
    export_normals = []


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
            face_lengths = []

            #process boundaries
            for surface in geom['boundaries']:
                #manage holes for triangulation
                if len(surface) > 1:
                    face_lengths = [ len(h) for h in surface ]
                    hole_indicies = itertools.accumulate(face_lengths)
                else:
                    hole_indicies = None
                    
                    #triangulate
                vertex_indices = np.array(surface).flatten()
                face_vertices = vertices[vertex_indices].flatten()
                face_normal, normal_exists = normal(face_vertices)
                    
                if not normal_exists:
                    raise Exception("The model contains face which couldn't be triangulated.")          
                    
                triangle_indices = earcut(face_vertices, hole_indicies, 3)
                    
                #transform to buffers
                buffer_vertices = np.array(vertices[vertex_indices][triangle_indices])
                buffer_normals = np.repeat([face_normal], len(triangle_indices), axis=0)    
                face_lengths.append(len(triangle_indices))
                export_vertices.append(buffer_vertices)
                export_normals.append(buffer_normals)


            #process semntaics
            if 'semantics' in geom:
                semantic_indices = geom['semantics']
                assert len(semantic_indices) == len(face_lengths)
                semantics = np.repeat(np.array(semantic_indices, dtype=np.int32), face_lengths)
            else:
                semantics = np.zeros((np.sum(face_lengths),), dtype=np.int32)

            #process parsed multisurface
            v = np.concatenate(export_vertices).flatten() 
            n = np.concatenate(export_normals).flatten()

            geometries.append({
                    'vertices': base64.b64encode(np.concatenate(export_vertices).flatten().astype(np.float32)),
                    'normals': base64.b64encode(np.concatenate(export_normals).flatten().astype(np.float32)),
                    'semantics': base64.b64encode(np.array(semantics).astype(np.int32)),
                })

            ##TODO WIP
            quit()



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

        #save merged geometries
        json.dump(geometries, geometry_file)




for file_name in tqdm(file_names):
    with open(os.path.join(objects_path, file_name), "r") as file:
        process_building_geometry(geometry_path, file, vertices, present_lods, stats, present_gtypes, file_name)



print(present_lods)
print(stats)
print(present_gtypes)
        



        










