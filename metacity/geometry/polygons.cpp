#include <stdexcept>
#include <unordered_map>
#include "polygons.hpp"
#include "triangulation.hpp"
#include "slicing.hpp"

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

shared_ptr<SimplePrimitive> MultiPolygon::transform() const
{
    vector<tvec3> vertices;
    Triangulator t;
    t.triangulate(polygons, vertices);
    return make_shared<SimpleMultiPolygon>(move(vertices));
}

//===============================================================================

SimpleMultiPolygon::SimpleMultiPolygon() : SimplePrimitive() {}
SimpleMultiPolygon::SimpleMultiPolygon(const vector<tvec3> & v) : SimplePrimitive(v) {}
SimpleMultiPolygon::SimpleMultiPolygon(const vector<tvec3> && v) : SimplePrimitive(move(v)) {}

shared_ptr<SimplePrimitive> SimpleMultiPolygon::copy() const
{
    auto cp = make_shared<SimpleMultiPolygon>();
    copy_to(cp);
    return cp;
}

shared_ptr<SimplePrimitive> SimpleMultiPolygon::transform() const
{
    return make_shared<SimpleMultiPolygon>(vertices);
}

const char * SimpleMultiPolygon::type() const
{
    return "simplepolygon";
}

inline tvec3 tcentroid(const tvec3 triangle[3])
{
    tvec3 c = triangle[0] + triangle[1] + triangle[2];
    c /= 3;
    return c;
}

void SimpleMultiPolygon::to_tiles(const std::vector<tvec3> &triangles, const float tile_size, Tiles & tiles) const
{
    Tiles::iterator search;
    pair<int, int> xy;

    for (size_t p = 0; p < triangles.size(); p += 3)
    {
        grid_coords(tcentroid(&triangles[p]), tile_size, xy);
        search = tiles.find(xy);
        if (search == tiles.end())
            search = tiles.insert({xy, make_shared<SimpleMultiPolygon>()}).first;
        search->second->push_vert(&triangles[p], 3);
    }
}

vector<shared_ptr<SimplePrimitive>> SimpleMultiPolygon::slice_to_grid(const float tile_size) const
{
    Tiles tiles;
    TriangleSlicer slicer;

    for (size_t i = 0; i < vertices.size(); i += 3)
    {
        slicer.grid_split(&vertices[i], tile_size);
        to_tiles(slicer.data(), tile_size, tiles);
    }

    vector<shared_ptr<SimplePrimitive>> tiled;
    for (const auto &tile : tiles)
        tiled.push_back(tile.second);

    return tiled;
}