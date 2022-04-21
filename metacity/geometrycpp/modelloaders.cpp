#include <stdexcept>
#include "modelloaders.hpp"
#include "points.hpp"
#include "segments.hpp"
#include "mesh.hpp"
#include "triangulation.hpp"

//===============================================================================

const char * MultiPoint::type() const {
    return "point";
}

void MultiPoint::push_p2(const vector<tfloat> iv)
{
    if (iv.size() % tvec2::length())
        throw runtime_error("Unexpected number of elements in input array");

    for (size_t i = 0; i < iv.size(); i += tvec2::length())
        points.emplace_back(iv[i], iv[i + 1], 0);
}

void MultiPoint::push_p3(const vector<tfloat> iv)
{
    if (iv.size() % tvec3::length())
        throw runtime_error("Unexpected number of elements in input array");

    for (size_t i = 0; i < iv.size(); i += tvec3::length())
        points.emplace_back(iv[i], iv[i + 1], iv[i + 2]);
}

shared_ptr<Model> MultiPoint::transform() const
{

    vector<tvec3> vertices;
    for(const auto & point : points)
        vertices.emplace_back(point);

    return make_shared<PointCloud>(move(vertices));
}


//===============================================================================


const char *MultiLine::type() const
{
    return "line";
}

void MultiLine::push_l2(const vector<tfloat> iv)
{
    if (iv.size() % tvec2::length() || (iv.size() < tvec2::length() * 2))
        throw runtime_error("Unexpected number of elements in input array");

    vector<tvec3> line;
    for (size_t i = 0; i < iv.size(); i += tvec2::length())
        line.emplace_back(iv[i], iv[i + 1], 0);
    lines.emplace_back(move(line));
}

void MultiLine::push_l3(const vector<tfloat> iv)
{
    if (iv.size() % tvec3::length() || (iv.size() < tvec3::length() * 2))
        throw runtime_error("Unexpected number of elements in input array");

    vector<tvec3> line;
    for (size_t i = 0; i < iv.size(); i += tvec3::length())
        line.emplace_back(iv[i], iv[i + 1], iv[i + 2]);
    lines.emplace_back(move(line));
}

shared_ptr<Model> MultiLine::transform() const
{
    vector<tvec3> vertices;
    for (const auto &line : lines)
    {
        if (line.size() < 2)
            continue;

        // append the first once
        vertices.emplace_back(line[0]);
        for (size_t i = 1; i < line.size() - 1; ++i)
        {
            // append the middle twice
            vertices.emplace_back(line[i]);
            vertices.emplace_back(line[i]);
        }
        // append the last only once
        vertices.emplace_back(line[line.size() - 1]);
    }

    return make_shared<Segments>(move(vertices));
}


//===============================================================================


const char *MultiPolygon::type() const
{
    return "polygon";
}

void MultiPolygon::push_p2(const vector<vector<tfloat>> ivertices)
{
    vector<vector<tvec3>> polygon;
    for (const auto &iring : ivertices)
    {
        if (iring.size() % tvec2::length())
            throw runtime_error("Unexpected number of elements in input array");

        if ((iring.size() / tvec2::length()) < 3) // only a single point or a line
            continue;

        vector<tvec3> ring;
        for (size_t i = 0; i < iring.size(); i += tvec2::length())
            ring.emplace_back(iring[i], iring[i + 1], 0);
        polygon.emplace_back(move(ring));
    }
    polygons.emplace_back(move(polygon));
}

void MultiPolygon::push_p3(const vector<vector<tfloat>> ivertices)
{
    vector<vector<tvec3>> polygon;
    for (const auto &iring : ivertices)
    {
        if (iring.size() % tvec3::length())
            throw runtime_error("Unexpected number of elements in input array");

        if ((iring.size() / tvec3::length()) < 3) // only a single point or a line
            continue;

        vector<tvec3> ring;
        for (size_t i = 0; i < iring.size(); i += tvec3::length())
            ring.emplace_back(iring[i], iring[i + 1], iring[i + 2]);
        polygon.emplace_back(move(ring));
    }
    polygons.emplace_back(move(polygon));
}


shared_ptr<Model> MultiPolygon::transform() const
{
    vector<tvec3> vertices;
    Triangulator t;
    t.triangulate(polygons, vertices);
    return make_shared<TriangularMesh>(move(vertices));
}
