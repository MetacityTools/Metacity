import numpy as np
import itertools
from earcut.earcut import earcut, normal
from models.model import FacetModel


def generate_hole_indices(surface):
    #manage holes for triangulation
    if len(surface) > 1:
        face_lengths = [ len(h) for h in surface ]
        face_length_sums = [ i for i in itertools.accumulate(face_lengths) ]
        return face_length_sums[:-1]
    else:
        return None


def triangulation_preprocess(vertices, surface):
    vertex_indices = np.array([ val for sublist in surface for val in sublist ]) #flatten irregular array
    face_vertices = vertices[vertex_indices].flatten()
    face_normal, normal_exists = normal(face_vertices)
                    
    if not normal_exists:  
        raise Exception("The model contains face which couldn't be triangulated.")
    return vertex_indices, face_vertices, face_normal


def triangulation_to_buffers(vertices, vertex_indices, triangle_indices, face_normal):
    buffer_vertices = np.array(vertices[vertex_indices][triangle_indices])
    buffer_normals = np.repeat([face_normal], len(triangle_indices), axis=0)    
    triangle_count = len(triangle_indices) 
    return buffer_vertices, buffer_normals, triangle_count


def face_to_buffers(vertices, surface):
    try:
        hole_indices = generate_hole_indices(surface)  
        vertex_indices, face_vertices, face_normal = triangulation_preprocess(vertices, surface)                        
        triangle_indices = earcut(face_vertices, hole_indices, 3)
        buffer_vertices, buffer_normals, triangle_count = triangulation_to_buffers(vertices, vertex_indices, triangle_indices, face_normal)
        return buffer_vertices, buffer_normals, triangle_count
    except:
        return np.array([]), np.array([]), 0


def process_model(vertices, boundaries, semantics):
    model = FacetModel()
    triangle_counts = []
    for surface in boundaries:
        buffer_vertices, buffer_normals, triangle_count = face_to_buffers(vertices, surface)
        model.vertices.extend(buffer_vertices)
        model.normals.extend(buffer_normals)
        triangle_counts.append(triangle_count)

    if semantics != None:
        assert len(semantics) == len(triangle_counts)
        model.semantics.extend(np.repeat(np.array(semantics, dtype=np.int32), triangle_counts))
    else:
        model.semantics.extend(np.zeros((np.sum(triangle_counts),), dtype=np.int32))

    return model

