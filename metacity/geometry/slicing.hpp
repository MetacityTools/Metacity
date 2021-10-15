#pragma once
#include "cgal.hpp"
#include "types.hpp"


class LineSlicer
{
public:
    void grid_split(const tvec3 line[2], const tfloat tile_size_);
    const vector<tvec3> & data();

protected:
    void setup(const tvec3 line[2], const tfloat tile_size_);
    pair<int, int> setup_range(const tvec3 line[2], tfloat tile_size, size_t axis);
    void intersect(const K::Plane_3 &plane, const K::Line_3 &ll);
    void insert_boundry_points(const tvec3 line[2]);
    void insert_along_axis(const pair<int, int> &range, size_t axis);

    vector<tvec3> points;
    pair<int, int> xrange;
    pair<int, int> yrange;
    tfloat tile_size;
    K::Line_3 splitted_line;
};

class TriangleSlicer
{
public:
    void grid_split(const tvec3 triangle[3], const tfloat tile_size_);
    const vector<tvec3> & data();

protected:
    // runtime routines
    void setup(const tvec3 t[3], const tfloat tile_size_);
    pair<int, int> setup_range(const tvec3 t[3], const tfloat tile_size, const size_t axis);
    tvec3 cross_point(const tvec3 &a, const tvec3 &b, const K::Plane_3 plane) const;
    void insert_triangle(const tvec3 triangle[3]);
    void insert_triangle_split(const tvec3 triangle[3]);
    void insert_triangle_split(const tvec3 &a, const tvec3 &b, const tvec3 &c);
    void one_on_plane_split(const tvec3 t[3], const K::Plane_3 &plane);
    void orinet(tvec3 t[3], const tfloat p, const size_t axis) const;
    inline void barrel_shift(tvec3 t[3]) const;
    // split routines
    void split_triangles_along_axis(const pair<int, int> &range, const size_t axis);
    void split_triangle_along_axis(const tvec3 triangle[3], const tfloat p, const K::Plane_3 &plane, const size_t axis);
    void general_case_split(const tvec3 t[3], const tfloat p, const K::Plane_3 &plane, const size_t axis);
    void special_case_split(const tvec3 t[3], const tfloat p, const K::Plane_3 &plane, const size_t axis);
    // predicates
    inline bool not_splitable(const tvec3 t[3], const tfloat &p, size_t axis) const;
    inline bool point_on_plane(const tvec3 t[3], const tfloat p, const size_t axis) const;
    inline bool bc_on_same_side(const tvec3 t[3], const tfloat p, const size_t axis) const;

    vector<tvec3> triangles;
    vector<tvec3> splited;
    pair<int, int> xrange;
    pair<int, int> yrange;
    tfloat tile_size;
};
