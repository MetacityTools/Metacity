
#include "types.hpp"
#include "cgal.hpp"
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;

tfloat interpolate_z(const tvec3 triangle[3], const K::Line_3 & line){
    K::Triangle_3 t = to_triangle(triangle);
    const auto res = CGAL::intersection(t, line);

    if (!res.is_initialized())
        return -FLT_MAX;

    if (const K::Point_3 *p = boost::get<K::Point_3>(&*res))
        return p->z();
        
    return -FLT_MAX;
}