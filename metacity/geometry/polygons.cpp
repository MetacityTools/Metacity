#include <stdexcept>
#include <unordered_map>
#include "primitives.hpp"
#include "triangulation.hpp"

//===============================================================================

SimpleMultiPolygon::SimpleMultiPolygon(const MultiPolygon & polygons)
: Primitive(polygons) {}

void SimpleMultiPolygon::transform()
{
    //nothing to do, already transformed
}

const char * SimpleMultiPolygon::type() const
{
    return "simplepolygon";
}

vector<shared_ptr<Primitive>> SimpleMultiPolygon::slice_to_grid(const float tile_size) const
{
    
}

//===============================================================================

const char * MultiPolygon::type() const {
    return "polygon";
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
    vector<vector<string>> vvspolygons;
    for (const auto &polygon : polygons)
    {
        vector<string> vspolygon;
        for (const auto &ring : polygon)
            vspolygon.emplace_back(vec_to_string(ring));
        vvspolygons.emplace_back(move(vspolygon));
    }

    json data = Primitive::serialize();
    data["polygons"] = vvspolygons;
    return data;
}


void MultiPolygon::deserialize(const json data)
{
    const auto vvspolygon = data.at("polygons").get<vector<vector<string>>>();
    for (const auto &vspolygon : vvspolygon)
    {
        vector<vector<tvec3>> vpolygon;
        for (const auto &sring : vspolygon)
            vpolygon.emplace_back(string_to_vec(sring));
        polygons.emplace_back(move(vpolygon));
    }

    Primitive::deserialize(data);
};

void MultiPolygon::transform()
{
    vertices.clear();
    Triangulator t;
    t.triangulate(polygons, vertices);
}

vector<shared_ptr<Primitive>> MultiPolygon::slice_to_grid(const float tile_size) const 
{
    SimpleMultiPolygon sp(*this);
    return sp.slice_to_grid(tile_size);
}