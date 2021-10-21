#include <stdexcept>
#include "glm/gtx/norm.hpp"
#include "slicing.hpp"

static K::Vector_3 axis_normal[2] = {K::Vector_3(1.0, 0, 0), K::Vector_3(0, 1.0, 0)};
static K::Vector_3 z_axis(0, 0, 1.0);

//===============================================================================

bool compare(const tvec3 &a, const tvec3 &b)
{
    if (a.x == b.x)
    {
        if (a.y == b.y)
            return a.z < b.z;
        return a.y < b.y;
    }
    return a.x < b.x;
}

//===============================================================================

const vector<tvec3> &LineSlicer::data()
{
    return points;
}

void LineSlicer::intersect(const K::Plane_3 &plane, const K::Line_3 &ll)
{
    const auto res = CGAL::intersection(plane, ll);

    if (!res.is_initialized())
        return;
        
    if (const K::Point_3 *p = boost::get<K::Point_3>(&*res))
        points.emplace_back(p->x(), p->y(), p->z());

}

void LineSlicer::insert_boundry_points(const tvec3 line[2])
{
    points.emplace_back(line[0]);
    points.emplace_back(line[1]);
}

bool LineSlicer::not_splitable(const tvec3 l[2], const tfloat &p, size_t axis) const
{
    return ((l[0][axis] <= p) && (l[1][axis] <= p)) ||
           ((l[0][axis] >= p) && (l[1][axis] >= p));
}

void LineSlicer::insert_along_axis(const tvec3 line[2], const pair<int, int> &range, size_t axis)
{
    tvec3 origin(0);
    for (int i = range.first; i <= range.second; ++i)
    {
        origin[axis] = i * tile_size;
        if (not_splitable(line, origin[axis], axis))
            continue;

        K::Plane_3 plane(to_point3(origin), axis_normal[axis]);
        intersect(plane, splitted_line);
    }
}

pair<int, int> LineSlicer::setup_range(const tvec3 line[2], tfloat tile_size, size_t axis)
{
    const auto range = minmax(line[0][axis], line[1][axis]);
    int base = range.first / tile_size;
    int stop = range.second / tile_size;
    return make_pair(base, stop);
}

void LineSlicer::setup(const tvec3 line[2], const tfloat tile_size_)
{
    points.clear();
    tile_size = tile_size_;
    xrange = setup_range(line, tile_size, 0);
    yrange = setup_range(line, tile_size, 1);
    splitted_line = K::Line_3(to_point3(line[0]), to_point3(line[1]));
}

void LineSlicer::grid_split(const tvec3 line[2], const tfloat tile_size_)
{
    setup(line, tile_size_);
    insert_boundry_points(line);

    // optimalization, check if there are any planes to intersect at all
    if (xrange.first > xrange.second && yrange.first > yrange.second)
        return;

    insert_along_axis(line, xrange, 0);
    insert_along_axis(line, yrange, 1);
    sort(points.begin(), points.end(), compare);
}

//===============================================================================

const vector<tvec3> &TriangleSlicer::data()
{
    return triangles;
}

// copied almost from line spliter
pair<int, int> TriangleSlicer::setup_range(const tvec3 t[3], const tfloat tile_size, const size_t axis)
{

    pair<tfloat, tfloat> range;
    //minimal axis
    range.first = min(t[0][axis], min(t[1][axis], t[2][axis]));
    //maximal axis
    range.second = max(t[0][axis], max(t[1][axis], t[2][axis]));
    
    int base = range.first / tile_size;
    int stop = range.second / tile_size;
    // in case the upper point is on the upper boundries, do not use them
    return make_pair(base, stop);
}

tvec3 TriangleSlicer::cross_point(const tvec3 &a, const tvec3 &b, const K::Plane_3 plane) const
{
    K::Line_3 ab(to_point3(a), to_point3(b));
    const auto res = CGAL::intersection(plane, ab);

    if (!res.is_initialized())
        throw runtime_error("No intersection: cross_point");

    if (const K::Point_3 *p = boost::get<K::Point_3>(&*res))
        return to_vec(*p);

    // in case all fails, use colinear point as backup
    // all fails usually means a and b lie both in the plane
    tvec3 backup = (a + b);
    backup *= 0.5;
    return backup;
}

void TriangleSlicer::setup(const tvec3 t[3], const tfloat tile_size_)
{
    triangles.clear();
    splited.clear();
    tile_size = tile_size_;
    xrange = setup_range(t, tile_size, 0);
    yrange = setup_range(t, tile_size, 1);
}

void TriangleSlicer::insert_triangle(const tvec3 triangle[3])
{
    triangles.insert(triangles.end(), triangle, triangle + 3);
}

void TriangleSlicer::insert_triangle_split(const tvec3 triangle[3])
{
    splited.insert(splited.end(), triangle, triangle + 3);
}

void TriangleSlicer::insert_triangle_split(const tvec3 &a, const tvec3 &b, const tvec3 &c)
{
    splited.emplace_back(a);
    splited.emplace_back(b);
    splited.emplace_back(c);
}

bool TriangleSlicer::not_splitable(const tvec3 t[3], const tfloat &p, size_t axis) const
{
    return ((t[0][axis] <= p) && (t[1][axis] <= p) && (t[2][axis] <= p)) ||
           ((t[0][axis] >= p) && (t[1][axis] >= p) && (t[2][axis] >= p));
}

bool TriangleSlicer::point_on_plane(const tvec3 t[3], const tfloat p, const size_t axis) const
{
    return (t[0][axis] == p) || (t[1][axis] == p) || (t[2][axis] == p);
}

void TriangleSlicer::one_on_plane_split(const tvec3 t[3], const K::Plane_3 &plane)
{
    tvec3 mid = cross_point(t[1], t[2], plane);
    insert_triangle_split(t[1], mid, t[0]);
    insert_triangle_split(t[0], mid, t[2]);
}

void TriangleSlicer::barrel_shift(tvec3 t[3]) const
{
    tvec3 x = t[0];
    t[0] = t[1];
    t[1] = t[2];
    t[2] = x;
}

void TriangleSlicer::special_case_split(const tvec3 t[3], const tfloat p, const K::Plane_3 &plane, const size_t axis)
{
    bool aop = (t[0][axis] == p);
    bool bop = (t[1][axis] == p);
    bool cop = (t[2][axis] == p);

    if (aop)
        return one_on_plane_split(t, plane);
    tvec3 copy[3] = {t[0], t[1], t[2]};
    barrel_shift(copy);
    if (bop)
        return one_on_plane_split(copy, plane);
    barrel_shift(copy);
    if (cop)
        return one_on_plane_split(copy, plane);
}

bool TriangleSlicer::bc_on_same_side(const tvec3 t[3], const tfloat p, const size_t axis) const
{
    bool b = (t[1][axis] < p);
    bool c = (t[2][axis] < p);
    return (b && c) || !(b || c);
}

void TriangleSlicer::orinet(tvec3 t[3], const tfloat p, const size_t axis) const
{
    size_t i = 0;
    while (!bc_on_same_side(t, p, axis))
    {
        ++i, barrel_shift(t);
        if (i > 3)
            throw runtime_error("We've got here some rolling triangles...");
    }
}

void TriangleSlicer::general_case_split(const tvec3 t[3], const tfloat p, const K::Plane_3 &plane, const size_t axis)
{
    tvec3 c[3] = {t[0], t[1], t[2]};
    orinet(c, p, axis);
    tvec3 mid_ab = cross_point(c[0], c[1], plane);
    tvec3 mid_ac = cross_point(c[0], c[2], plane);
    tfloat dist_ab_c = glm::length2(c[2] - mid_ab);
    tfloat dist_b_ac = glm::length2(c[1] - mid_ac);

    if (dist_ab_c > dist_b_ac)
    {
        insert_triangle_split(c[0], mid_ab, mid_ac);
        insert_triangle_split(mid_ab, c[1], mid_ac);
        insert_triangle_split(c[1], c[2], mid_ac);
    }
    else
    {
        insert_triangle_split(c[0], mid_ab, mid_ac);
        insert_triangle_split(mid_ab, c[1], c[2]);
        insert_triangle_split(mid_ab, c[2], mid_ac);
    }
}

void TriangleSlicer::split_triangle_along_axis(const tvec3 triangle[3], const tfloat p, const K::Plane_3 &plane, const size_t axis)
{
    if (not_splitable(triangle, p, axis))
        return insert_triangle_split(triangle);

    if (point_on_plane(triangle, p, axis))
        special_case_split(triangle, p, plane, axis);
    else
        general_case_split(triangle, p, plane, axis);
}

void TriangleSlicer::split_triangles_along_axis(const pair<int, int> &range, const size_t axis)
{
    tvec3 origin(0);
    for (int i = range.first; i <= range.second; ++i)
    {
        splited.clear();
        origin[axis] = (tfloat)(i) * tile_size;
        K::Plane_3 plane(to_point3(origin), axis_normal[axis]);
        for (size_t i = 0; i < triangles.size(); i += 3)
            split_triangle_along_axis(&triangles[i], origin[axis], plane, axis);
        triangles = splited;
    }
}

void TriangleSlicer::grid_split(const tvec3 triangle[3], const tfloat tile_size_)
{
    setup(triangle, tile_size_);
    insert_triangle(triangle);

    //optimalization, check if there are any planes to intersect at all
    if (xrange.first == xrange.second && yrange.first == yrange.second)
        return;

    split_triangles_along_axis(xrange, 0);
    split_triangles_along_axis(yrange, 1);
}

//===============================================================================

const vector<tvec3> &TriangleOverlay::data()
{
    return out_triangles;
}

void TriangleOverlay::segment(const K::Triangle_2 &target_)
{
    target = target_;
    out_triangles.clear();

    if (source.is_degenerate() || target.is_degenerate())
        return;

    if (source_proj.is_degenerate())
        handle_degenerate();
    else
        handle_general();
}

bool TriangleOverlay::handle_general()
{

    const auto res = CGAL::intersection(source_proj, target);
    tmp_points.clear();

    if (!res.is_initialized())
        return false;

    if (const vector<K::Point_2> *v = boost::get<vector<K::Point_2>>(&*res))
    {
        project_vertices(v->data(), v->size(), source.supporting_plane());
        return handle_vertices(tmp_points);
    }

    if (const K::Triangle_2 *t = boost::get<K::Triangle_2>(&*res))
    {
        project_triangle(*t, source.supporting_plane());
        return handle_vertices(tmp_points);
    }

    return false;
}

void TriangleOverlay::set_source(const tvec3 triangle[3])
{
    source = to_triangle(triangle);
    source_proj = to_triangle2(triangle);

    if (source_proj.is_degenerate())
        source_proj_segment = to_segment2(source_proj);
}

K::Segment_2 TriangleOverlay::to_segment2(const K::Triangle_2 & t2)
{
    if (t2[0] < t2[1])
    {
        if (t2[1] < t2[2])
            return K::Segment_2(t2[0], t2[2]);
        if (t2[0] < t2[2])
            return K::Segment_2(t2[0], t2[1]);
        return K::Segment_2(t2[2], t2[1]);
    }
    else
    {
        if (t2[0] < t2[2])
            return K::Segment_2(t2[1], t2[2]);
        if (t2[1] < t2[2])
            return K::Segment_2(t2[1], t2[0]);
        return K::Segment_2(t2[2], t2[0]);
    }
}

bool TriangleOverlay::handle_triangle(const K::Triangle_3 &t)
{
    out_triangles.push_back(to_vec(t[0]));
    out_triangles.push_back(to_vec(t[1]));
    out_triangles.push_back(to_vec(t[2]));
    return true;
}

bool TriangleOverlay::handle_vertices(const vector<K::Point_3> &v)
{
    triangulator.triangulate(v, out_triangles);
    return true;
}

bool TriangleOverlay::handle_deg_2_to_3(const K::Segment_2 *ps)
{
    const K::Point_3 a = to_point3(ps->min());
    const K::Point_3 b = to_point3(ps->max());
    K::Vector_3 ab_normal(a, b);
    K::Vector_3 ba_normal(b, a);
    const K::Plane_3 ab(a, ba_normal); //negative side to the middle
    const K::Plane_3 ba(b, ab_normal);

    Mesh m;
    m.add_face(m.add_vertex(source[0]), m.add_vertex(source[1]), m.add_vertex(source[2]));

    CGAL::Polygon_mesh_processing::clip(m, ab);
    CGAL::Polygon_mesh_processing::remove_degenerate_faces(m);
    CGAL::Polygon_mesh_processing::clip(m, ba);
    CGAL::Polygon_mesh_processing::remove_degenerate_faces(m);


    for (const Mesh::Face_index & face_index : m.faces()) {
        CGAL::Vertex_around_face_circulator<Mesh> vcirc(m.halfedge(face_index), m);
        CGAL::Vertex_around_face_circulator<Mesh> done(vcirc);
        do {
            out_triangles.emplace_back(to_vec(m.point(*vcirc++)));
        }  while (vcirc != done);
    }

    return true;
}

bool TriangleOverlay::handle_degenerate()
{
    const auto res = CGAL::intersection(source_proj_segment, target);
    if (!res.is_initialized())
        return false;

    if (const K::Segment_2 *projected_intersection = boost::get<K::Segment_2>(&*res))
        return handle_deg_2_to_3(projected_intersection);
    return false;
}

void TriangleOverlay::project_point2(const K::Point_2 &point, const K::Plane_3 &plane)
{
    K::Line_3 line(to_point3(point), z_axis);
    const auto res = CGAL::intersection(plane, line);

    if (!res.is_initialized())
        throw runtime_error("No intersection: project_point2");

    if (const K::Point_3 *v = boost::get<K::Point_3>(&*res))
        tmp_points.push_back(*v);
}

void TriangleOverlay::project_vertices(const K::Point_2 *verts, size_t size, const K::Plane_3 &plane)
{
    for (size_t i = 0; i < size; ++i)
        project_point2(verts[i], plane);
}

void TriangleOverlay::project_triangle(const K::Triangle_2 &t, const K::Plane_3 &plane)
{
    project_point2(t[0], plane);
    project_point2(t[1], plane);
    project_point2(t[2], plane);
}