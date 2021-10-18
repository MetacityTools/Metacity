#include <stdexcept>
#include <iostream>
#include "slicing.hpp"
#include "lines.hpp"
#include "rtree.hpp"

static K::Vector_3 z_axis(0, 0, 1);

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

shared_ptr<SimplePrimitive> MultiLine::transform() const
{
    vector<tvec3> vertices;
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

    return make_shared<SimpleMultiLine>(move(vertices));
}

//===============================================================================

SimpleMultiLine::SimpleMultiLine() : SimplePrimitive() {}
SimpleMultiLine::SimpleMultiLine(const vector<tvec3> & v) : SimplePrimitive(v) {}
SimpleMultiLine::SimpleMultiLine(const vector<tvec3> && v) : SimplePrimitive(move(v)) {}


shared_ptr<SimplePrimitive> SimpleMultiLine::copy() const
{
    auto cp = make_shared<SimpleMultiLine>();
    copy_to(cp);
    return cp;
}


shared_ptr<SimplePrimitive> SimpleMultiLine::transform() const
{
    return make_shared<SimpleMultiLine>(vertices);
}

const char *SimpleMultiLine::type() const
{
    return "simpleline";
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
            
        search->second->push_vert(&points[p], 2);
    }
}

vector<shared_ptr<SimplePrimitive>> SimpleMultiLine::slice_to_grid(const float tile_size) const
{
    Tiles tiles;
    LineSlicer slicer;

    for (size_t i = 0; i < vertices.size(); i += 2)
    {
        slicer.grid_split(&vertices[i], tile_size);
        to_tiles(slicer.data(), tile_size, tiles);
    }

    vector<shared_ptr<SimplePrimitive>> tiled;
    for (const auto &tile : tiles)
        tiled.push_back(tile.second);

    return tiled;
}

bool get_segment(const tvec3 triangle[3], const K::Plane_3 & plane, const K::Iso_cuboid_3 & cuboid, tvec3 & a, tvec3 & b)
{
    K::Triangle_3 t = to_triangle(triangle);
    const auto res1 = CGAL::intersection(t, plane);

    if (!res1.is_initialized())
        return false;

    if (const K::Segment_3 *s = boost::get<K::Segment_3>(&*res1))
    {
        const auto res2 = CGAL::intersection(*s, cuboid);

        if (!res2.is_initialized())
            return false;

        if (const K::Segment_3 *s = boost::get<K::Segment_3>(&*res1))
        {
            a = to_vec(s->min());
            b = to_vec(s->max());
            return true;
        }
    }
    return false;
}

void SimpleMultiLine::map(const shared_ptr<SimpleMultiPolygon> target) 
{
    if (!(mapping_ready() && target->mapping_ready()))
        throw runtime_error("Either mapped primitives are not ready for mapping (most likely miss the attribute OID.");

    //helpers
    tvec3 la, lb;
    vector<size_t> indices;
    BBox box;
    uint32_t noidtmp;
    RTree tree(target);

    //data
    vector<tvec3> nvertices;
    const shared_ptr<TAttribute<uint32_t>> target_oid = static_pointer_cast<TAttribute<uint32_t>>(target->attribute("oid"));
    const shared_ptr<TAttribute<uint32_t>> source_oid = static_pointer_cast<TAttribute<uint32_t>>(attrib["oid"]);
    shared_ptr<TAttribute<uint32_t>> ntarget_oid = make_shared<TAttribute<uint32_t>>();
    shared_ptr<TAttribute<uint32_t>> nsource_oid = make_shared<TAttribute<uint32_t>>();


    for(size_t l = 0; l < vertices.size(); l += 2)
    {
        indices.clear();
        la = vertices[l];
        lb = vertices[l + 1];

        //ignore vertical or degenerate lines
        if (la.z == lb.z)
            continue;

        for_line(&vertices[l], box);
        tree.range_query(box, indices);

        if (indices.size() > 0)
        {
            K::Plane_3 plane(to_point3(la), to_point3(lb), to_point3(la) + z_axis);
            K::Iso_cuboid_3 cuboid(K::Point_3(la.x, la.y, FLT_MIN), K::Point_3(lb.x, lb.y, FLT_MAX));
            for(const auto & i : indices)
            {
                //caution, reusing la, lb to save registers...
                if(get_segment(target->triangle(i), plane, cuboid, la, lb))
                {
                    nvertices.emplace_back(la);
                    nvertices.emplace_back(lb);
                    noidtmp = (*target_oid)[i * 3];
                    ntarget_oid->emplace_back(noidtmp);
                    ntarget_oid->emplace_back(noidtmp);
                    noidtmp = (*source_oid)[l];
                    nsource_oid->emplace_back(noidtmp);
                    nsource_oid->emplace_back(noidtmp);
                }
            }
        }
    }

    init_proxy(nsource_oid, ntarget_oid, nvertices);
}