#include "cgal.hpp"
#include "slicing.hpp"
#include <iostream>

using namespace std;


int main(int argc, char const *argv[])
{
    const auto v1 = tvec3(10, 0, 1);
    const auto v2 = tvec3(13, 0, 2);
    const auto v3 = tvec3(11.5, 2.5, 3);
    const tvec3 vt3[3] = {v1, v2, v3};

    TriangleOverlay t;
    t.set_source(vt3);

    K::Triangle_2 b(K::Point_2(0, 2), K::Point_2(3, 2), K::Point_2(1.5, -1));
    for (size_t i = 0; i < 100000; i++)
    {
        t.segment(b);
        /* code */
    }

    return 0;
}
