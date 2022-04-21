#include <stdexcept>
#include <numeric>
#include "models.hpp"
#include "triangulation.hpp"
#include "bbox.hpp"
#include "cppcodec/base64_rfc4648.hpp"
//===============================================================================

BaseModel::~BaseModel() {}

void BaseModel::add_tag(const string key, const int32_t value)
{
    tags[key] = value;
}

json BaseModel::get_tags() const
{
    return tags;
}

//===============================================================================
Model::Model() : BaseModel() {}
Model::Model(const vector<tvec3> &v) : BaseModel(), vertices(v) {}
Model::Model(const vector<tvec3> &&v) : BaseModel(), vertices(v) {}

tuple<tfloat, tfloat, tfloat> Model::centroid() const
{
    tvec3 c = accumulate(vertices.begin(), vertices.end(), tvec3(0));
    c /= vertices.size();
    return make_tuple(c.x, c.y, c.z);
}

tuple<tuple<tfloat, tfloat, tfloat>, tuple<tfloat, tfloat, tfloat>> Model::bounding_box() const
{
    BBox box;
    set_empty(box);
    for (const tvec3 &v : vertices)
        extend(box, v);
    return make_tuple(make_tuple(box.min.x, box.min.y, box.min.z), make_tuple(box.max.x, box.max.y, box.max.z));
}

void Model::shift(const tfloat sx, const tfloat sy, const tfloat sz)
{
    const tvec3 shift(sx, sy, sz);
    for (tvec3 &v : vertices)
        v += shift;
}

void Model::deserialize(const json data)
{
    data.at("tags").get_to(tags);
    const auto sverts = data.at("vertices").get<string>();
    vertices = string_to_vec(sverts);

    for (const auto &attr : data.at("attributes").items())
        attrib[attr.key()] = attr_deserialize(attr.value());
}

json Model::serialize() const
{
    json data = {
        {"tags", tags},
        {"type", type()},
        {"vertices", vec_to_string(vertices)}};

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

void Model::copy_to(shared_ptr<Model> cp) const
{
    cp->vertices = vertices;
    cp->tags = tags;
    for (const auto &a : attrib)
        cp->attrib[a.first] = a.second->copy();
}
