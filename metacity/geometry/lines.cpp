#include <stdexcept>
#include <iostream>
#include "slicing.hpp"
#include "primitives.hpp"

//===============================================================================

SimpleMultiLine::SimpleMultiLine()
    : Primitive() {}

SimpleMultiLine::SimpleMultiLine(const MultiLine &lines)
    : Primitive(lines) {}

void SimpleMultiLine::transform()
{
    //nothing to do, already transformed
}

const char *SimpleMultiLine::type() const
{
    return "simpleline";
}

ostream & operator<<(ostream & os, const tvec3 & vec)
{
    os << vec.x << " " << vec.y << " " << vec.z;
    return os;
}

ostream & operator<<(ostream & os, const vector<tvec3> & vec)
{
    os << "[\n";
    for (const auto & v: vec )
        os << "   " << v << "\n";
    os << "]";
    return os;
}

void SimpleMultiLine::to_tiles(const std::vector<tvec3> &points, const float tile_size, Tiles & tiles) const
{
    Tiles::iterator search;
    pair<int, int> xy;

    for (size_t p = 0; p < points.size() - 1; ++p)
    {
        grid_coords(points[p], tile_size, xy);
        search = tiles.find(xy);
        if (search == tiles.end())
            search = tiles.insert({xy, make_shared<SimpleMultiLine>()}).first;
            
        search->second->push_vert(points[p], points[p + 1]);
    }
}

vector<shared_ptr<Primitive>> SimpleMultiLine::slice_to_grid(const float tile_size) const
{
    Tiles tiles;
    LineSlicer slicer;

    for (size_t i = 0; i < vertices.size(); i += 2)
    {
        slicer.grid_split(make_pair(vertices[i], vertices[i + 1]), tile_size);
        to_tiles(slicer.res(), tile_size, tiles);
    }

    vector<shared_ptr<Primitive>> tiled;
    for (const auto &tile : tiles)
        tiled.push_back(tile.second);

    return tiled;
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
    vector<string> vsline;

    for (const auto &line : lines)
        vsline.emplace_back(vec_to_string(line));

    json data = Primitive::serialize();
    data["lines"] = vsline;
    return data;
}

void MultiLine::deserialize(const json data)
{
    const auto vslines = data.at("lines").get<vector<string>>();
    for (const auto &sline : vslines)
        lines.emplace_back(string_to_vec(sline));
    Primitive::deserialize(data);
};

void MultiLine::transform()
{
    vertices.clear();
    for (const auto &line : lines)
    {
        auto p = line.begin();
        //append the first once
        vertices.emplace_back(*p);
        const auto last_but_one = prev(line.end());
        for (p++; p != last_but_one; p++)
        {
            //append the middle twice
            vertices.emplace_back(*p);
            vertices.emplace_back(*p);
        }
        //append the last only once
        vertices.emplace_back(*p);
    }
}

vector<shared_ptr<Primitive>> MultiLine::slice_to_grid(const float tile_size) const
{
    SimpleMultiLine sl(*this);
    return sl.slice_to_grid(tile_size);
}
