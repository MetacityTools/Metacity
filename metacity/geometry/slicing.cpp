#include "slicing.hpp"

static K::Vector_3 xaxis(1.0, 0, 0);
static K::Vector_3 yaxis(0, 1.0, 0);

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

pair<int, int> LineSlicer::setup_range(pair<const tfloat &, const tfloat &> range, tfloat tile_size)
{
    int base = (range.first / tile_size) + 1;
    int stop = range.second / tile_size;
    tfloat upper = tile_size * stop;

    //in case the upper point is on the upper boundries, do not use them
    if (range.first <= upper && range.second <= upper)
        stop--;

    return make_pair(base, stop);
}

const vector<tvec3> &LineSlicer::res()
{
    return points;
}

void LineSlicer::intersect(const K::Plane_3 &plane, const K::Line_3 &ll)
{
    const auto res = CGAL::intersection(plane, ll);

    if (const K::Point_3 *p = boost::get<K::Point_3>(&*res))
        points.emplace_back(p->x(), p->y(), p->z());
}

void LineSlicer::grid_split(const line &l, const tfloat tile_size)
{
    points.clear();

    const auto xrange = minmax(l.first.x, l.second.x);
    const auto yrange = minmax(l.first.y, l.second.y);
    pair<int, int> xsplits = setup_range(xrange, tile_size);
    pair<int, int> ysplits = setup_range(yrange, tile_size);
    points.emplace_back(l.first);
    points.emplace_back(l.second);

    //optimalization, check if there are any planes to intersect at all
    if (xsplits.first > xsplits.second && ysplits.first > ysplits.second)
        return;

    K::Line_3 splitted_line(K::Point_3(l.first.x, l.first.y, l.first.z),
                            K::Point_3(l.second.x, l.second.y, l.second.z));

    for (int i = xsplits.first; i <= xsplits.second; ++i)
    {
        const auto plane = K::Plane_3(K::Point_3(i * tile_size, 0, 0), xaxis);
        intersect(plane, splitted_line);
    }

    for (int i = ysplits.first; i <= ysplits.second; ++i)
    {
        const auto plane = K::Plane_3(K::Point_3(0, i * tile_size, 0), yaxis);
        intersect(plane, splitted_line);
    }

    sort(points.begin(), points.end(), compare);
}

class TriangleSlicer {

    //copied
    pair<int, int> setup_range(pair<const tfloat &, const tfloat &> range, tfloat tile_size)
    {
        int base = (range.first / tile_size) + 1;
        int stop = range.second / tile_size;
        tfloat upper = tile_size * stop;

        //in case the upper point is on the upper boundries, do not use them
        if (range.first <= upper && range.second <= upper)
            stop--;

        return make_pair(base, stop);
    }


    void grid_split(const triangle & t, const tfloat tile_size) 
    {
        pair<tfloat, tfloat> xrange;
        xrange.first = min(get<1>(t).x, min(get<0>(t).x, get<1>(t).x));
        xrange.second = max(get<1>(t).x, max(get<0>(t).x, get<1>(t).x));
        pair<tfloat, tfloat> yrange;
        yrange.first = min(get<1>(t).y, min(get<0>(t).y, get<1>(t).y));
        yrange.second = max(get<1>(t).y, max(get<0>(t).y, get<1>(t).y));

        pair<int, int> xsplits = setup_range(xrange, tile_size);
        pair<int, int> ysplits = setup_range(yrange, tile_size);

        //optimalization, check if there are any planes to intersect at all
        if (xsplits.first > xsplits.second && ysplits.first > ysplits.second)
            return;


        //TODO
    }
};
 