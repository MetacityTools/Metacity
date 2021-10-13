#pragma once
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Segment_3.h>
#include <CGAL/intersections.h>
#include <boost/variant.hpp>
#include "types.hpp"

using line = pair<tvec3, tvec3>;
using triangle = tuple<tvec3, tvec3, tvec3>;

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;


class LineSlicer {
public:
    void grid_split(const line & l, const tfloat tile_size);
    const vector<tvec3> & res();

protected:
    pair<int, int> setup_range(pair<const float &, const float &> range, tfloat tile_size);
    void intersect(const K::Plane_3 & plane, const K::Line_3 & ll);

    vector<tvec3> points;
};
