#include "bbox.hpp"

//pass

std::ostream &operator<<(std::ostream &os, const tvec3 &v)
{
    os << "[" << v.x << ", " << v.y << ", " << v.z << "]";
    return os;
}
std::ostream &operator<<(std::ostream &os, const BBox &b){
    os << "[" << b.min << ", " << b.max << "]";
    return os;
}