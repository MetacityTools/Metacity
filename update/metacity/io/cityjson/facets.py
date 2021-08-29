import itertools
from typing import Iterable, List, Union

import numpy as np
import numpy.typing as npt
from earcut.earcut import earcut, normal
from metacity.datamodel.primitives.facets import FacetModel


TVertices = npt.NDArray[np.float32]
TNormals = npt.NDArray[np.float32]
TBoundaries = List[List[List[int]]]
TSurface = List[List[int]]
TSemantics = Union[List[int], None]
TIndices = Iterable[int]



class CJFacetParser:
    def __init__(self, vertices: TVertices, boundaries: TBoundaries, semantics: TSemantics):
        self.vertices = vertices
        self.boundaries = boundaries
        self.semantics = semantics


    def parse(self):
        vs, ns = [], []
        triangle_counts = []   
        for surface in self.boundaries:
            try:
                v, n, tc = self.face_to_buffers(surface)
                vs.extend(v)
                ns.extend(n)
                triangle_counts.append(tc)
            except: 
                pass

        return self.assemble_model(vs, ns, triangle_counts)


    def assemble_model(self, vertices, normals, triangle_counts):
        model = FacetModel()
        model.vertices = np.array(vertices, dtype=np.float32)
        model.normals = np.array(normals, dtype=np.float32)
        model.semantics = self.transformed_semantics(triangle_counts)
        return model


    def face_to_buffers(self, surface: TSurface):
        self.generate_hole_indices(surface)  
        self.triangulation_preprocess(surface)  
        self.triangle_indices = earcut(self.face_vertices, self.hole_indices, 3)
        return self.triangulation_to_buffers()


    def generate_hole_indices(self, surface: TSurface):
        #manage holes for triangulation
        if len(surface) > 1:
            face_lengths = [ len(h) for h in surface ]
            face_length_sums = [ i for i in itertools.accumulate(face_lengths) ]
            self.hole_indices = face_length_sums[:-1]
        else:
            self.hole_indices = None


    def triangulation_preprocess(self, surface: TSurface):
        self.vertex_indices = np.array([ val for sublist in surface for val in sublist ]) #flatten irregularly-shaped list of lists
        self.face_vertices = self.vertices[self.vertex_indices].flatten()
        self.face_normal, normal_exists = normal(self.face_vertices)
                        
        if not normal_exists:  
            raise Exception("The model contains face which couldn't be triangulated.")


    def triangulation_to_buffers(self):
        used_vertices = self.vertices[self.vertex_indices]
        vertices = np.array(used_vertices[self.triangle_indices])
        normals = np.repeat([self.face_normal], len(self.triangle_indices), axis=0)    
        tri_count = len(self.triangle_indices) 
        return vertices, normals, tri_count


    def transformed_semantics(self, triangle_counts):
        if self.semantics != None:
            assert len(self.semantics) == len(triangle_counts)
            return np.repeat(np.array(self.semantics, dtype=np.int32), triangle_counts)
        else:
            return np.zeros((np.sum(triangle_counts),), dtype=np.int32) - 1



