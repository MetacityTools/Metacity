import numpy as np



def buffers_to_stl(flat_vertices, flat_normals, filename):
    with open(filename, "w") as file:
        file.write("solid model\n")

        verts = flat_vertices.reshape((flat_vertices.shape[0] // 9, 3, 3))
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

        file.write("solid model\n")