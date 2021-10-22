#include <stdexcept>
#include <numeric>
#include "primitives.hpp"
#include "triangulation.hpp"
#include "bbox.hpp"
#include "cppcodec/base64_rfc4648.hpp"
//===============================================================================
//JSON merging 
//did I actually finish this?
//contains does not work

void merge_tags(json & ltags, const json & rtags)
{
    for (const auto & it : rtags.items())
    {
        const auto key = it.key();
        if (ltags.contains(it.key()))
        {
            auto lv = ltags[key];
            const auto rv = it.value();
            if (lv.is_array() && rv.is_array())
            {
                for(const auto & v: rv)
                {
                    if(!lv.contains(v))
                        lv.push_back(v);
                }
            } 
            else if (lv.is_array() && !rv.is_array())
            {
                if(!lv.contains(rv))
                    lv.push_back(rv);
            }
            else if (!lv.is_array() && rv.is_array())
            {
                lv = json::array({lv});
                for(const auto & v: rv)
                {
                    if(!lv.contains(v))
                        lv.push_back(v);
                }
            } else {
                if (lv != rv)
                    lv = json::array({lv, rv});
            }

            ltags[key] = lv;
        } else {
            ltags[key] = it.value();
        }
    }
}

//===============================================================================

Primitive::~Primitive() {}

void Primitive::deserialize(const json data)
{
    data.at("tags").get_to(tags);
}

json Primitive::serialize() const
{
    return {
        {"tags", tags},
        {"type", type()}};
}

//===============================================================================
SimplePrimitive::SimplePrimitive() : Primitive() {}
SimplePrimitive::SimplePrimitive(const vector<tvec3> &v) : Primitive(), vertices(v) {}
SimplePrimitive::SimplePrimitive(const vector<tvec3> &&v) : Primitive(), vertices(v) {}

tuple<tfloat, tfloat, tfloat> SimplePrimitive::centroid() const
{
    tvec3 c = centroidvec();
    return make_tuple(c.x, c.y, c.z);
}

tvec3 SimplePrimitive::centroidvec() const
{
    tvec3 c = accumulate(vertices.begin(), vertices.end(), tvec3(0));
    c /= vertices.size();
    return c;
}

tuple<tuple<tfloat, tfloat, tfloat>, tuple<tfloat, tfloat, tfloat>> SimplePrimitive::bounding_box() const
{
    BBox box;
    set_empty(box);
    for (const tvec3 & v: vertices)
        extend(box, v);
    return make_tuple(make_tuple(box.min.x, box.min.y, box.min.z), make_tuple(box.max.x, box.max.y, box.max.z));
}


void SimplePrimitive::shift(const tfloat sx, const tfloat sy, const tfloat sz)
{   
    const tvec3 shift(sx, sy, sz); 
    for (tvec3 & v: vertices)
        v += shift;
}

void SimplePrimitive::join(const shared_ptr<SimplePrimitive> primitive)
{
    for (const auto & attr: attrib)
    {
        const auto it = primitive->attrib.find(attr.first);
        if (primitive->attrib.end() == it)
            throw runtime_error("RHS of SimplePrimitive join is missing attribute: " + attr.first);
        attr.second->join(it->second);
    }

    vertices.insert(vertices.end(), primitive->vertices.begin(), primitive->vertices.end());
    merge_tags(tags, primitive->tags);
}

void SimplePrimitive::push_vert(const tvec3 &vec)
{
    vertices.emplace_back(vec);
}

void SimplePrimitive::push_vert(const tvec3 *vec, size_t count)
{
    vertices.insert(vertices.end(), vec, vec + count);
}

void SimplePrimitive::deserialize(const json data)
{
    Primitive::deserialize(data);
    const auto sverts = data.at("vertices").get<string>();
    vertices = string_to_vec(sverts);

    for (const auto &attr : data.at("attributes").items())
        attrib[attr.key()] = attr_deserialize(attr.value());
}

json SimplePrimitive::serialize() const
{
    json data = Primitive::serialize();
    data["vertices"] = vec_to_string(vertices);
    json sattrib = json::object({});

    for (const auto &attr : attrib)
        sattrib.update({{attr.first, attr.second->serialize()}});

    data["attributes"] = sattrib;
    return data;
}

void SimplePrimitive::add_attribute(const string &name, const uint32_t value)
{
    auto attr = make_shared<TAttribute<uint32_t>>();
    attr->clear();
    attr->fill(value, vertices.size());
    attrib[name] = attr;
}

void SimplePrimitive::add_attribute(const string &name, const shared_ptr<Attribute> attr)
{
    attrib[name] = attr;
}

shared_ptr<SimplePrimitive> SimplePrimitive::transform() const {
    return copy();
}

void SimplePrimitive::copy_to(shared_ptr<SimplePrimitive> cp) const
{
    cp->vertices = vertices;
    cp->tags = tags;
    for (const auto & a: attrib)
        cp->attrib[a.first] = a.second->copy();
}

bool SimplePrimitive::mapping_ready() const
{
    const auto it = attrib.find("oid");
    return it != attrib.end();
}

void SimplePrimitive::init_proxy(const shared_ptr<TAttribute<uint32_t>> soid, const shared_ptr<TAttribute<uint32_t>> toid, const vector<tvec3> & nv)
{
    attrib.clear();
    attrib["source_oid"] = soid;
    attrib["oid"] = toid;
    tags["proxy"] = true;
    vertices = nv;
}
