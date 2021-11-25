#include <stdexcept>
#include <numeric>
#include "models.hpp"
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

BaseModel::~BaseModel() {}

void BaseModel::deserialize(const json data)
{
    data.at("tags").get_to(tags);
}

json BaseModel::serialize() const
{
    return {
        {"tags", tags},
        {"type", type()}};
}

//===============================================================================
Model::Model() : BaseModel() {}
Model::Model(const vector<tvec3> &v) : BaseModel(), vertices(v) {}
Model::Model(const vector<tvec3> &&v) : BaseModel(), vertices(v) {}

tuple<tfloat, tfloat, tfloat> Model::centroid() const
{
    tvec3 c = centroidvec();
    return make_tuple(c.x, c.y, c.z);
}

tvec3 Model::centroidvec() const
{
    tvec3 c = accumulate(vertices.begin(), vertices.end(), tvec3(0));
    c /= vertices.size();
    return c;
}

tuple<tuple<tfloat, tfloat, tfloat>, tuple<tfloat, tfloat, tfloat>> Model::bounding_box() const
{
    BBox box;
    set_empty(box);
    for (const tvec3 & v: vertices)
        extend(box, v);
    return make_tuple(make_tuple(box.min.x, box.min.y, box.min.z), make_tuple(box.max.x, box.max.y, box.max.z));
}


void Model::shift(const tfloat sx, const tfloat sy, const tfloat sz)
{   
    const tvec3 shift(sx, sy, sz); 
    for (tvec3 & v: vertices)
        v += shift;
}

void Model::join(const shared_ptr<Model> model)
{
    for (const auto & attr: attrib)
    {
        const auto it = model->attrib.find(attr.first);
        if (model->attrib.end() == it)
            throw runtime_error("RHS of Model Join is missing attribute: " + attr.first);
        attr.second->join(it->second);
    }

    vertices.insert(vertices.end(), model->vertices.begin(), model->vertices.end());
    merge_tags(tags, model->tags);
}

void Model::push_vert(const tvec3 &vec)
{
    vertices.emplace_back(vec);
}

void Model::push_vert(const tvec3 *vec, size_t count)
{
    vertices.insert(vertices.end(), vec, vec + count);
}

void Model::deserialize(const json data)
{
    BaseModel::deserialize(data);
    const auto sverts = data.at("vertices").get<string>();
    vertices = string_to_vec(sverts);

    for (const auto &attr : data.at("attributes").items())
        attrib[attr.key()] = attr_deserialize(attr.value());
}

json Model::serialize() const
{
    json data = BaseModel::serialize();
    data["vertices"] = vec_to_string(vertices);
    json sattrib = json::object({});

    for (const auto &attr : attrib)
        sattrib.update({{attr.first, attr.second->serialize()}});

    data["attributes"] = sattrib;
    return data;
}

json Model::serialize_stream() const
{
    json data = BaseModel::serialize();
    data["vertices"] = vec_to_f_to_string(vertices);
    json sattrib = json::object({});

    for (const auto &attr : attrib)
        sattrib.update({{attr.first, attr.second->serialize()}});

    data["attributes"] = sattrib;
    return data;
}

void Model::add_attribute(const string &name, const uint32_t value)
{
    auto attr = make_shared<TAttribute<uint32_t>>();
    attr->clear();
    attr->fill(value, vertices.size());
    attrib[name] = attr;
}

void Model::add_attribute(const string &name, const shared_ptr<Attribute> attr)
{
    attrib[name] = attr;
}

shared_ptr<Model> Model::transform() const {
    return copy();
}

void Model::copy_to(shared_ptr<Model> cp) const
{
    cp->vertices = vertices;
    cp->tags = tags;
    for (const auto & a: attrib)
        cp->attrib[a.first] = a.second->copy();
}

bool Model::mapping_ready() const
{
    const auto it = attrib.find("oid");
    return it != attrib.end();
}

void Model::init_proxy(const shared_ptr<TAttribute<uint32_t>> soid, const shared_ptr<TAttribute<uint32_t>> toid, const vector<tvec3> & nv)
{
    attrib.clear();
    attrib["source_oid"] = soid;
    attrib["oid"] = toid;
    tags["proxy"] = true;
    vertices = nv;
}
