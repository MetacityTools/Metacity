#include <stdexcept>
#include <unordered_map>
#include "primitives.hpp"

//===============================================================================

SimpleMultiPoint::SimpleMultiPoint() 
: Primitive() {}

SimpleMultiPoint::SimpleMultiPoint(const MultiPoint & points)
: Primitive(points) {}

void SimpleMultiPoint::transform()
{
    //nothing to do, already transformed
}

const char * SimpleMultiPoint::type() const
{
    return "simplepoint";
}

vector<shared_ptr<Primitive>> SimpleMultiPoint::slice_to_grid(const float tile_size) const
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

    vector<shared_ptr<Primitive>> tiled;
    for (const auto & tile : tiles) 
        tiled.push_back(tile.second);

    return tiled;
}

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

vector<tfloat> MultiPoint::contents() const
{
    return vec_to_float(points);
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

void MultiPoint::transform()
{
    vertices.clear();
    for(const auto & point : points)
        vertices.emplace_back(point);
}


vector<shared_ptr<Primitive>> MultiPoint::slice_to_grid(const float tile_size) const 
{
    SimpleMultiPoint sp(*this);
    return sp.slice_to_grid(tile_size);
}

//===============================================================================
