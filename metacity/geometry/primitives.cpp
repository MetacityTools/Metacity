#include <stdexcept>
#include "primitives.hpp"
#include "cppcodec/base64_rfc4648.hpp"


Primitive::~Primitive() {}

vector<tfloat> Primitive::vec_to_float(const vector<tvec3> &vec) const
{
    vector<tfloat> c;
    for (const auto &v : vec)
    {
        c.push_back(v.x);
        c.push_back(v.y);
        c.push_back(v.z);
    }

    return c;
}

void Primitive::append(vector<uint8_t> &vec, tfloat f) const
{
    uint8_t * d = (uint8_t *) &f; 
    vec.insert(vec.end(), d, d + 4);
}

vector<uint8_t> Primitive::vec_to_unit8(const vector<tvec3> &vec) const
{
    vector<uint8_t> bytes;
    bytes.reserve(3 * sizeof(tfloat) * vec.size());
    
    for (const auto &v : vec)
    {
        append(bytes, v.x);
        append(bytes, v.y);
        append(bytes, v.z);
    }

    return bytes;
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

vector<tfloat> MultiPoint::contents() const
{
    return vec_to_float(points);
}

json MultiPoint::serialize() const
{
    vector<uint8_t> pointsui8 = vec_to_unit8(points);

    using base64 = cppcodec::base64_rfc4648;
    string pointss = base64::encode(&pointsui8[0], pointsui8.size());

    return {
        {"points", pointss},
        {"type", "point"}
    };
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

vector<vector<tfloat>> MultiLine::contents() const
{
    vector<vector<tfloat>> c;
    for (const auto &l : lines)
    {
        vector<tfloat> lp = vec_to_float(l);
        c.emplace_back(move(lp));
    }

    return c;
}

json MultiLine::serialize() const
{

}

void MultiPolygon::push_p2(const vector<vector<tfloat>> ivertices)
{
    vector<vector<tvec3>> polygon;
    for (const auto &iring : ivertices)
    {
        if (iring.size() % tvec2::length())
            throw runtime_error("Unexpected number of elements in input array");

        if (iring.size() / tvec2::length() < 3) // only a single point or a line
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

        if (iring.size() / tvec3::length() < 3) // only a single point or a line
            continue;

        vector<tvec3> ring;
        for (size_t i = 0; i < iring.size(); i += tvec3::length())
            ring.emplace_back(iring[i], iring[i + 1], iring[i + 2]);
        polygon.emplace_back(move(ring));
    }
    polygons.emplace_back(move(polygon));
}

vector<vector<vector<tfloat>>> MultiPolygon::contents() const
{
    vector<vector<vector<tfloat>>> c;
    for (const auto &p : polygons)
    {
        vector<vector<tfloat>> pr;
        for (const auto &r : p)
        {
            vector<tfloat> cr = vec_to_float(r);
            pr.emplace_back(move(cr));
        }
        c.emplace_back(move(pr));
    }
    return c;
}

json MultiPolygon::serialize() const
{
    
}
