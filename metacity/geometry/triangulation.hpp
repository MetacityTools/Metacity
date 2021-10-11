#pragma once
#include <vector>

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/Polygon_mesh_processing/orient_polygon_soup.h>
#include <CGAL/Polygon_mesh_processing/polygon_soup_to_polygon_mesh.h>
#include <CGAL/Polygon_mesh_processing/compute_normal.h>
#include <CGAL/Plane_3.h>

#include "mapbox/earcut.hpp"
#include "primitives.hpp"
using namespace std;


typedef vector<vector<tvec3>> Polygon;
typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Surface_mesh<K::Point_3> Mesh;
typedef vector<vector<tvec3>> Polygon;
typedef vector<vector<vector<tvec3>>> Polygons;


class Triangulator {
public:
    Triangulator() {};
    void triangulate(const Polygons & in_polygons, vector<tvec3> & out_vertices);

protected:
    Mesh mesh;
    vector<vector<K::Point_2>> projected;
    vector<Mesh::Vertex_index> tmp_points;
    vector<Mesh::Face_index> tmp_faces;
    vector<tvec3> vertexrefs;
    K::Vector_3 normal;

    void to_cgal_mesh(const Polygons &polygons);
    void compute_normal(const Mesh::Face_index fi);
    void project_pair(const Polygon &polygon, vector<tvec3> & out_vertices);
};



