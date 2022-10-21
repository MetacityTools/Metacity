#pragma once
#include "../types.hpp"
#include <iostream>

struct BBox
{
    BBox() : min(FLT_MAX), max(-FLT_MAX) {}
    BBox(tvec3 _min, tvec3 _max) : min(_min), max(_max) {}

    tvec3 min;
    tvec3 max;

    inline tvec3 centroid() const
    {
        return (min + max) * tvec3(0.5);
    }

    void set_empty()
    {
        min = tvec3(FLT_MAX);
        max = tvec3(-FLT_MAX);
    }

    inline void for_triangle(const tvec3 & a, const tvec3 & b, const tvec3 & c)
    {
        for (int i = 0; i < 3; i++) {
            min[i] = std::min(a[i], std::min(b[i], c[i]));
            max[i] = std::max(a[i], std::max(b[i], c[i]));
        }
    }

    inline void for_line(const tvec3 l[2])
    {
        min.x = std::min(l[0].x, l[1].x);
        min.y = std::min(l[0].y, l[1].y);
        min.z = std::min(l[0].z, l[1].z);
        max.x = std::max(l[0].x, l[1].x);
        max.y = std::max(l[0].y, l[1].y);
        max.z = std::max(l[0].z, l[1].z);
    }

    inline void for_bboxes(const BBox &b1, const BBox &b2)
    {
        min.x = std::min(b1.min.x, b2.min.x);
        min.y = std::min(b1.min.y, b2.min.y);
        min.z = std::min(b1.min.z, b2.min.z);
        max.x = std::max(b1.max.x, b2.max.x);
        max.y = std::max(b1.max.y, b2.max.y);
        max.z = std::max(b1.max.z, b2.max.z);
    }

    inline bool overlaps(const BBox &b2) const
    {
        // If one rectangle is on left side of other       or above
        return !(b2.max.x <= min.x || max.x <= b2.min.x || b2.max.y <= min.y || max.y <= b2.min.y);
    }


    inline bool overlaps(const tvec3 & a, const tvec3 & b, const tvec3 & c) const
    {
        BBox box_tri;
        box_tri.for_triangle(a, b, c);
        return overlaps(box_tri);
    }

    inline bool inside(const tvec3 &p) const
    {
        return ((min.x <= p.x) && (p.x < max.x)) && ((min.y <= p.y) && (p.y < max.y));
    }

    inline void extend(const BBox &b2)
    {
        min.x = std::min(min.x, b2.min.x);
        min.y = std::min(min.y, b2.min.y);
        min.z = std::min(min.z, b2.min.z);
        max.x = std::max(max.x, b2.max.x);
        max.y = std::max(max.y, b2.max.y);
        max.z = std::max(max.z, b2.max.z);
    }

    inline void extend(const tvec3 &p)
    {
        min.x = std::min(min.x, p.x);
        min.y = std::min(min.y, p.y);
        min.z = std::min(min.z, p.z);
        max.x = std::max(max.x, p.x);
        max.y = std::max(max.y, p.y);
        max.z = std::max(max.z, p.z);
    }

    inline void toEqualXY()
    {
        tvec3 mid = centroid();
        tfloat hx = (max.x - min.x) / 2;
        tfloat hy = (max.y - min.y) / 2;
        tfloat rad = std::max(hx, hy);
        min.x = mid.x - rad;
        min.y = mid.y - rad;
        max.x = mid.x + rad;
        max.y = mid.y + rad;
    }

    inline tfloat midpoint(uint8_t axis) const
    {
        return (min[axis] + max[axis]) / 2;
    }
};

std::ostream &operator<<(std::ostream &os, const tvec3 &v);
std::ostream &operator<<(std::ostream &os, const BBox &b);
