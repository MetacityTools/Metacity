#include <stdexcept>
#include <unordered_map>
#include "points.hpp"

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

json MultiPoint::serialize() const
{
    json data = Primitive::serialize();
    data["points"] = vec_to_string(points);
    return data;
}

void MultiPoint::deserialize(const json data)
{
    const auto spoints = data.at("points").get<string>();
    points = string_to_vec(spoints);
    Primitive::deserialize(data);
};

shared_ptr<SimplePrimitive> MultiPoint::transform() const
{

    vector<tvec3> vertices;
    for(const auto & point : points)
        vertices.emplace_back(point);

    return make_shared<SimpleMultiPoint>(move(vertices));
}


//===============================================================================

SimpleMultiPoint::SimpleMultiPoint() : SimplePrimitive() {}
SimpleMultiPoint::SimpleMultiPoint(const vector<tvec3> & v) : SimplePrimitive(v) {}
SimpleMultiPoint::SimpleMultiPoint(const vector<tvec3> && v) : SimplePrimitive(move(v)) {}

shared_ptr<SimplePrimitive> SimpleMultiPoint::copy() const
{
    auto cp = make_shared<SimpleMultiPoint>();
    copy_to(cp);
    return cp;
}

shared_ptr<SimplePrimitive> SimpleMultiPoint::transform() const
{
    //nothing to do, already transformed
    return make_shared<SimpleMultiPoint>(vertices);
}

const char * SimpleMultiPoint::type() const
{
    return "simplepoint";
}

vector<shared_ptr<SimplePrimitive>> SimpleMultiPoint::slice_to_grid(const float tile_size) const
{
    Tiles tiles;
    Tiles::iterator search;
    pair<int, int> xy;

    for(const auto & v : vertices)
    {
        grid_coords(v, tile_size, xy);
        search = tiles.find(xy);
        if (search == tiles.end())
            search = tiles.insert({xy, make_shared<SimpleMultiPoint>()}).first;
        search->second->push_vert(v);
    }

    vector<shared_ptr<SimplePrimitive>> tiled;
    for (const auto & tile : tiles) 
        tiled.push_back(tile.second);

    return tiled;
}
