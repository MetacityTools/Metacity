from metacity.helpers.iter import ensure_list_like
from typing import Iterable, List, TextIO, Union

import numpy as np
from metacity.models.object import MetacityObject


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


def export_objects_stl(file: Union[TextIO, List[TextIO]],  objects: Iterable[MetacityObject], lod: Union[int, List[int]]):
    file = ensure_list_like(file)
    lod = ensure_list_like(lod)

    for obj in objects:
        for output_file, l in zip(file, lod):
            model = obj.facets.lod[l]
            if model.exists:
                buffers_to_stl(model.vertices, model.normals, obj.oid, output_file)

    

