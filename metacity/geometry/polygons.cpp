#include <stdexcept>
#include <unordered_map>
#include <fstream>
#include "polygons.hpp"
#include "rtree.hpp"
#include "triangulation.hpp"
#include "slicing.hpp"

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
SimpleMultiPolygon::SimpleMultiPolygon(const vector<tvec3> &v) : SimplePrimitive(v) {}
SimpleMultiPolygon::SimpleMultiPolygon(const vector<tvec3> &&v) : SimplePrimitive(move(v)) {}

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

const char *SimpleMultiPolygon::type() const
{
    return "simplepolygon";
}

size_t SimpleMultiPolygon::to_obj(const string & path, const size_t offset) const 
{
    ofstream objfile(path, std::ios_base::app);
    objfile << "o Polygon" << offset << endl; 
    for(const auto & v: vertices)
        objfile << "v " << v.x << " " << v.y << " " << v.z << endl;

    for(size_t i = offset + 1; i < offset + 1 + vertices.size(); i += 3)
        objfile << "f " << i << " " << i + 1 << " " << i + 2 << endl;

    objfile.close();
    return vertices.size();
}

inline tvec3 tcentroid(const tvec3 triangle[3])
{
    tvec3 c = triangle[0] + triangle[1] + triangle[2];
    c /= 3;
    return c;
}

void SimpleMultiPolygon::to_tiles(const std::vector<tvec3> &triangles, const float tile_size, Tiles &tiles) const
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

const tvec3 * SimpleMultiPolygon::triangle(const size_t index) const
{
    return &(vertices[index * 3]);
}

const shared_ptr<Attribute> SimpleMultiPolygon::attribute(const string & name)
{
    const auto it = attrib.find(name);
    if (it == attrib.end())
        throw runtime_error("The primitive is missing attribute " + name);
    return it->second;
}

void SimpleMultiPolygon::map(const shared_ptr<SimpleMultiPolygon> target) 
{
    if (!(mapping_ready() && target->mapping_ready()))
        throw runtime_error("Either mapped primitives are not ready for mapping (most likely miss the attribute OID.");

    //helpers
    BBox box;
    vector<size_t> indices;
    uint32_t source_oid_value, target_oid_value;
    RTree tree(target);
    TriangleOverlay overlay;

    //data
    vector<tvec3> nvertices;
    const shared_ptr<TAttribute<uint32_t>> target_oid = static_pointer_cast<TAttribute<uint32_t>>(target->attribute("oid"));
    const shared_ptr<TAttribute<uint32_t>> source_oid = static_pointer_cast<TAttribute<uint32_t>>(attrib["oid"]);
    shared_ptr<TAttribute<uint32_t>> ntarget_oid = make_shared<TAttribute<uint32_t>>();
    shared_ptr<TAttribute<uint32_t>> nsource_oid = make_shared<TAttribute<uint32_t>>();


    for(size_t t = 0; t < vertices.size(); t += 3)
    {
        indices.clear();
        for_triangle(&vertices[t], box);
        tree.range_query(box, indices);

        if (indices.size() > 0)
        {
            overlay.set_source(&vertices[t]);
            for(const auto & i : indices)
            {
                overlay.segment(to_triangle2(target->triangle(i)));
                source_oid_value = (*source_oid)[t];
                target_oid_value = (*target_oid)[i * 3];
                
                const auto & d = overlay.data();
                if (d.size() >= 3)
                {
                    nvertices.insert(nvertices.end(), d.begin(), d.end());
                    ntarget_oid->fill((*target_oid)[i * 3], d.size());
                    nsource_oid->fill((*source_oid)[t], d.size());
                }
            }
        }
    }

    init_proxy(nsource_oid, ntarget_oid, nvertices);
}