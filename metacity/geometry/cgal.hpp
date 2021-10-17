#pragma once
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/intersections.h>
#include <CGAL/Surface_mesh.h>
//#include <CGAL/Polygon_mesh_processing/orient_polygon_soup.h>
//#include <CGAL/Polygon_mesh_processing/polygon_soup_to_polygon_mesh.h>
#include <CGAL/Polygon_mesh_processing/compute_normal.h>
#include <boost/variant.hpp>
#include "glm/glm.hpp"

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Surface_mesh<K::Point_3> Mesh;

inline K::Point_3 to_point3(const glm::vec3 &v)
{
    return K::Point_3(v.x, v.y, v.z);
}

inline K::Point_2 to_point2(const glm::vec3 &v)
{
    return K::Point_2(v.x, v.y);
}

inline K::Triangle_3 to_triangle(const glm::vec3 triangle[3])
{
    return K::Triangle_3(to_point3(triangle[0]), to_point3(triangle[1]), to_point3(triangle[2]));
}

inline K::Triangle_2 to_triangle2(const glm::vec3 triangle[3])
{
    return K::Triangle_2(to_point2(triangle[0]), to_point2(triangle[1]), to_point2(triangle[2]));
}

inline glm::vec3 to_vec(const K::Point_3 &p)
{
    return glm::vec3(p.x(), p.y(), p.z());
}

inline K::Point_3 to_point3(const K::Point_2 &p)
{
    return K::Point_3(p.x(), p.y(), 0);
}