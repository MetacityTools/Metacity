#include <stdexcept>
#include "glm/gtx/norm.hpp"
#include "slicing.hpp"

static K::Vector_3 axis_normal[2] = {K::Vector_3(1.0, 0, 0), K::Vector_3(0, 1.0, 0)};

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

inline K::Point_3 to_point3(const tvec3 &v)
{
    return K::Point_3(v.x, v.y, v.z);
}

inline tvec3 to_vec(const K::Point_3 &p)
{
    return tvec3(p.x(), p.y(), p.z());
}

ostream & operator<<(ostream & os, const tvec3 & vec)
{
    os << vec.x << " " << vec.y << " " << vec.z;
    return os;
}

ostream & operator<<(ostream & os, const vector<tvec3> & vec)
{
    os << "[\n";
    for (const auto & v: vec )
        os << "   " << v << "\n";
    os << "]";
    return os;
}

//===============================================================================

const vector<tvec3> & LineSlicer::data(){
    return points;
}

void LineSlicer::intersect(const K::Plane_3 &plane, const K::Line_3 &ll)
{
    const auto res = CGAL::intersection(plane, ll);
    if (const K::Point_3 *p = boost::get<K::Point_3>(&*res))
        points.emplace_back(p->x(), p->y(), p->z());
}

void LineSlicer::insert_boundry_points(const tvec3 line[2])
{
    points.emplace_back(line[0]);
    points.emplace_back(line[0]);
}

void LineSlicer::insert_along_axis(const pair<int, int> &range, size_t axis)
{
    tvec3 origin(0);
    for (int i = range.first; i <= range.second; ++i)
    {
        origin[axis] = i * tile_size;
        K::Plane_3 plane(to_point3(origin), axis_normal[axis]);
        intersect(plane, splitted_line);
    }
}

pair<int, int> LineSlicer::setup_range(const tvec3 line[2], tfloat tile_size, size_t axis)
{
    const auto range = minmax(line[0][axis], line[1][axis]);
    int base = (range.first / tile_size) + 1;
    int stop = range.second / tile_size;
    tfloat upper = tile_size * stop;

    // in case the upper point is on the upper boundries, do not use them
    if (range.first <= upper && range.second <= upper)
        stop--;

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

    insert_along_axis(xrange, 0);
    insert_along_axis(yrange, 1);
    sort(points.begin(), points.end(), compare);
}

//===============================================================================

const vector<tvec3> & TriangleSlicer::data(){
    return triangles;
}

// copied almost from line spliter
pair<int, int> TriangleSlicer::setup_range(const tvec3 t[3], const tfloat tile_size, const size_t axis)
{
    pair<tfloat, tfloat> range;
    range.first =  min(t[0][axis], min(t[1][axis], t[2][axis]));
    range.second = max(t[0][axis], max(t[1][axis], t[2][axis]));

    int base = (range.first / tile_size) + 1;
    int stop = range.second / tile_size;
    tfloat upper = tile_size * stop;

    // in case the upper point is on the upper boundries, do not use them
    if (range.first <= upper && range.second <= upper)
        stop--;

    return make_pair(base, stop);
}

tvec3 TriangleSlicer::cross_point(const tvec3 &a, const tvec3 &b, const K::Plane_3 plane) const
{
    K::Line_3 ab(to_point3(a), to_point3(b));
    const auto res = CGAL::intersection(plane, ab);

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
    splited.insert(triangles.end(), triangle, triangle + 3);
}

void TriangleSlicer::insert_triangle_split(const tvec3 &a, const tvec3 &b, const tvec3 &c)
{
    splited.emplace_back(a);
    splited.emplace_back(b);
    splited.emplace_back(c);
}

inline bool TriangleSlicer::not_splitable(const tvec3 t[3], const tfloat &p, size_t axis) const
{
    return ((t[0][axis] <= p) && (t[1][axis] <= p) && (t[2][axis] <= p)) ||
           ((t[0][axis] >= p) && (t[1][axis] >= p) && (t[2][axis] >= p));
}

inline bool TriangleSlicer::point_on_plane(const tvec3 t[3], const tfloat p, const size_t axis) const
{
    return (t[0][axis] == p) || (t[1][axis] == p) || (t[2][axis] == p);
}

void TriangleSlicer::one_on_plane_split(const tvec3 t[3], const K::Plane_3 &plane)
{
    tvec3 mid = cross_point(t[1], t[2], plane);
    insert_triangle_split(t[1], mid, t[0]);
    insert_triangle_split(t[0], mid, t[2]);
}

inline void TriangleSlicer::barrel_shift(tvec3 t[3]) const
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

inline bool TriangleSlicer::bc_on_same_side(const tvec3 t[3], const tfloat p, const size_t axis) const
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
            throw runtime_error("rolling triangles");
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
        origin[axis] = i * tile_size;
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

    // optimalization, check if there are any planes to intersect at all
    if (xrange.first > xrange.second && yrange.first > yrange.second)
        return;

    split_triangles_along_axis(xrange, 0);
    split_triangles_along_axis(yrange, 1);
}