#include <stdexcept>
#include <unordered_map>
#include "points.hpp"
#include "cgal.hpp"
#include "rtree.hpp"

static K::Vector_3 z_axis(0, 0, 1.0);

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

const char * SimpleMultiPoint::type() const
{
    return "simplepoint";
}

size_t SimpleMultiPoint::to_obj(const string & path, const size_t offset) const 
{
    ofstream objfile(path, std::ios_base::app);
    objfile << "o PointCloud" << offset << endl; 
    for(const auto & v: vertices)
        objfile << "v " << v.x << " " << v.y << " " << v.z << endl;
    objfile.close();
    return vertices.size();
}

vector<shared_ptr<SimplePrimitive>> SimpleMultiPoint::slice_to_grid(const tfloat tile_size) const
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

tfloat interpolate_z(const tvec3 triangle[3], const K::Line_3 & line)
{
    K::Triangle_3 t = to_triangle(triangle);
    const auto res = CGAL::intersection(t, line);

    if (!res.is_initialized())
        return -FLT_MAX;

    if (const K::Point_3 *p = boost::get<K::Point_3>(&*res))
        return p->z();
        
    return -FLT_MAX;
}

void SimpleMultiPoint::map(const shared_ptr<SimpleMultiPolygon> target) 
{
    if (!(mapping_ready() && target->mapping_ready()))
        throw runtime_error("Either mapped primitives are not ready for mapping (most likely miss the attribute OID.");

    //helpers
    tfloat z, maxz;
    tvec3 v;
    size_t best;
    vector<size_t> indices;
    RTree tree(target);

    //data
    vector<tvec3> nvertices;
    const shared_ptr<TAttribute<uint32_t>> target_oid = static_pointer_cast<TAttribute<uint32_t>>(target->attribute("oid"));
    const shared_ptr<TAttribute<uint32_t>> source_oid = static_pointer_cast<TAttribute<uint32_t>>(attrib["oid"]);
    shared_ptr<TAttribute<uint32_t>> ntarget_oid = make_shared<TAttribute<uint32_t>>();
    shared_ptr<TAttribute<uint32_t>> nsource_oid = make_shared<TAttribute<uint32_t>>();
    
    for(size_t p = 0; p < vertices.size(); ++p)
    {   
        indices.clear();
        v = vertices[p];

        tree.point_query(v, indices);
        maxz = -FLT_MAX;

        if (indices.size() > 0)
        {
            K::Line_3 line(to_point3(v), z_axis);
            for(const auto & i : indices)
            {
                z = interpolate_z(target->triangle(i), line);
                if (z > maxz)
                {
                    best = i;
                    maxz = z;
                }
            }

            if (maxz != -FLT_MAX)
            {
                v.z = maxz;
                nvertices.emplace_back(v);
                ntarget_oid->emplace_back((*target_oid)[best * 3]);
                nsource_oid->emplace_back((*source_oid)[p]);
            }
        }
    }

    init_proxy(nsource_oid, ntarget_oid, nvertices);
}