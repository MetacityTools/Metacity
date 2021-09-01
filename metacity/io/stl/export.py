import numpy as np


def ensure_list_like(data):
    if isinstance(data, list) or isinstance(data, tuple):
        return data
    return [data]


def export_buffers(flat_v, flat_n, name, file, shift=np.array([0, 0, 0])):
    file.write(f"solid {name}\n")

    verts = flat_v.reshape((flat_v.shape[0] // 9, 3, 3))
    verts = verts - shift
    norms = flat_n.reshape((flat_n.shape[0] // 9, 3, 3))

    for tv, tn in zip(verts, norms):
        file.write("    facet normal ")
        for i in range(3):
            file.write(str(tn[0][i]))
            file.write(" ")
        file.write("\n")

        file.write("       outer loop\n")
        for i in range(3):
            file.write(f"          vertex {tv[i][0]} {tv[i][1]} {tv[i][2]}\n")
        file.write("       endloop\n")
        file.write("    endfacet\n")

    file.write(f"endsolid {name}\n")
