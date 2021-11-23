#pragma once
#include <vector>
#include "mapbox/earcut.hpp"
#include "cgal.hpp"
#include "types.hpp"


using namespace std;

class Triangulator {
public:
    Triangulator() {};
    void triangulate(const TPolygons & in_polygons, vector<tvec3> & out_vertices);
    void triangulate(const TCGALFlatPolygon & in_polygon, vector<tvec3> & out_vertices);

protected:
    Mesh mesh;
    vector<vector<K::Point_2>> projected;
    vector<Mesh::Vertex_index> tmp_points;
    vector<Mesh::Face_index> tmp_faces;
    vector<tvec3> vertexrefs;
    K::Vector_3 normal;

    bool to_cgal_mesh(const TPolygon &polygon);
    bool to_cgal_mesh(const TCGALFlatPolygon &polygon);
    void compute_normal(const Mesh::Face_index fi);
    void project_pair(const TPolygon &polygon);
    void project_pair(const TCGALFlatPolygon &polygon);
};



