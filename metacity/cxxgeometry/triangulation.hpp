#pragma once
#include <vector>
#include "mapbox/earcut.hpp"
#include "cgal.hpp"
#include "types.hpp"


using namespace std;

using SimplePolygon = vector<K::Point_3>;

class Triangulator {
public:
    Triangulator() {};
    void triangulate(const Polygons & in_polygons, vector<tvec3> & out_vertices);
    void triangulate(const SimplePolygon & in_polygon, vector<tvec3> & out_vertices);

protected:
    Mesh mesh;
    vector<vector<K::Point_2>> projected;
    vector<Mesh::Vertex_index> tmp_points;
    vector<Mesh::Face_index> tmp_faces;
    vector<tvec3> vertexrefs;
    K::Vector_3 normal;

    bool to_cgal_mesh(const Polygon &polygon);
    bool to_cgal_mesh(const SimplePolygon &polygon);
    void compute_normal(const Mesh::Face_index fi);
    void project_pair(const Polygon &polygon);
    void project_pair(const SimplePolygon &polygon);
};



