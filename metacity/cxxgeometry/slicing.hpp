#pragma once
#include "cgal.hpp"
#include "types.hpp"
#include "triangulation.hpp"


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
    void insert_along_axis(const tvec3 line[2], const pair<int, int> &range, size_t axis);
    bool not_splitable(const tvec3 t[2], const tfloat &p, size_t axis) const;

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
    void barrel_shift(tvec3 t[3]) const;
    // split routines
    void split_triangles_along_axis(const pair<int, int> &range, const size_t axis);
    void split_triangle_along_axis(const tvec3 triangle[3], const tfloat p, const K::Plane_3 &plane, const size_t axis);
    void general_case_split(const tvec3 t[3], const tfloat p, const K::Plane_3 &plane, const size_t axis);
    void special_case_split(const tvec3 t[3], const tfloat p, const K::Plane_3 &plane, const size_t axis);
    // predicates
    bool not_splitable(const tvec3 t[3], const tfloat &p, size_t axis) const;
    bool point_on_plane(const tvec3 t[3], const tfloat p, const size_t axis) const;
    bool bc_on_same_side(const tvec3 t[3], const tfloat p, const size_t axis) const;

    vector<tvec3> triangles;
    vector<tvec3> splited;
    pair<int, int> xrange;
    pair<int, int> yrange;
    tfloat tile_size;
};


class TriangleOverlay {
public:
    void set_source(const tvec3 triangle[3]);
    //now this is the reall stuff looking like it's nothing:
    //a) set_source has to be called before you call segment
    //b) it intersects 2D projection of source with the parameter of segment and projects the result back to 3D
    //it handles degenerate cases, such as degenerate triangles, degenerate 
    //2D projection (aka vetical source triangles), the 2D intersections are correctly 
    //interpolated back to 3D in EVERY case I could think of, it's a freaking masterpiece
    //
    //the bad news is it's not really optimal implementation
    //I tried to maximize the performance while still maintaining the code readable, 
    //which is freaking difficult when you got million special cases
    //anyone is more than welcome to optimize all of this
    //I dare you to try
    //and yes you have to use CGAL, we keep it robust here
    void segment(const K::Triangle_2 & target_);
    const vector<tvec3> & data();

protected:
    bool handle_general();
    bool handle_degenerate();

    K::Segment_2 to_segment2(const K::Triangle_2 & t2);
    bool handle_triangle(const K::Triangle_3 & t);
    bool handle_vertices(const vector<K::Point_3> & v);
    bool handle_deg_2_to_3(const K::Segment_2 * ps);
    
    void project_vertices(const K::Point_2 * verts, size_t size, const K::Plane_3 & plane);
    void project_triangle(const K::Triangle_2 & t, const K::Plane_3 & plane);
    void project_point2(const K::Point_2 & point, const K::Plane_3 & plane);

    K::Triangle_3 source;
    K::Triangle_2 source_proj;
    K::Segment_2 source_proj_segment;
    K::Triangle_2 target;
    Triangulator triangulator;
    vector<K::Point_3> tmp_points;
    vector<tvec3> out_triangles;
};
