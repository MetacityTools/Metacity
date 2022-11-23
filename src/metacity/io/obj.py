from typing import List
from metacity.geometry import Attribute, Model, Progress


def swapYZ(file_in: str, file_out: str):
    with open(file_in, 'r') as f:
        lines = f.readlines()
    contents = ""

    for line in lines:
        if line.startswith('v '):
            line = line.split()
            line[2], line[3] = str(-float(line[3])), line[2]
            line = " ".join(line) + "\n"
            contents += line
        else:
            contents += line

    with open(file_out, 'w') as f:
        f.write(contents)


def load_obj(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()
    vertices = []
    faces = []
    for line in lines:
        if line.startswith('v '):
            vertices.append([float(x) for x in line.split()[1:]])
        elif line.startswith('f '):
            faces.append([int(x.split('/')[0]) for x in line.split()[1:]])
    return vertices, faces


def obj_data_to_polygons(vertices: List[List[float]], faces: List[List[int]]):
    polygons = []
    for face in faces:
        polygon = []
        for i in face:
            polygon.extend(vertices[i - 1])
        polygons.append([polygon])
    return polygons


def parse(file: str, progress: Progress = None):
    vertices, faces = load_obj(file)
    polygons = obj_data_to_polygons(vertices, faces)
    model = Model()
    attr = Attribute()
    for polygon in polygons:
        attr.push_polygon3D(polygon)
        progress.update()
    model.add_attribute('POSITION', attr)
    return [model]