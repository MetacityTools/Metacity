import json

import numpy as np
from models.model import FacetModel, NonFacetModel


#export
def buffers_to_stl(flat_vertices, flat_normals, model_name, file, shift = np.array([0, 0, 0])):  
    file.write(f"solid {model_name}\n")

    verts = flat_vertices.reshape((flat_vertices.shape[0] // 9, 3, 3))
    verts = verts - shift
    norms = flat_normals.reshape((flat_normals.shape[0] // 9, 3, 3))

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

    file.write(f"endsolid {model_name}\n")


def load_model(file):
    try:
        contents = json.load(file)
    except:
        with open(file, 'r') as local_file:
            contents = json.load(local_file)
    
    if 'normals' in contents:
        model = FacetModel()
    else:
        model = NonFacetModel()
    model.deserialize(contents)
    return model 


def load_models(files):
    models = []
    for file in files:
        models.append(load_model(file))
    return models

    





