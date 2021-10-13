#include <stdexcept>
#include <unordered_map>
#include "primitives.hpp"
#include "triangulation.hpp"
#include "cppcodec/base64_rfc4648.hpp"

Primitive::~Primitive() {}

vector<tfloat> Primitive::vec_to_float(const vector<tvec3> &vec) const
{
    vector<tfloat> c;
    for (const auto &v : vec)
    {
        c.push_back(v.x);
        c.push_back(v.y);
        c.push_back(v.z);
    }

    return c;
}

void Primitive::append(vector<uint8_t> &vec, tfloat f) const
{
    uint8_t *d = (uint8_t *)&f;
    vec.insert(vec.end(), d, d + 4);
}

void Primitive::grid_coords(const tvec3 &point, const float tile_size, pair<int, int> &coords) const
{
    coords.first = (point.x / tile_size);
    coords.second = (point.y / tile_size);
}

vector<uint8_t> Primitive::vec_to_unit8(const vector<tvec3> &vec) const
{
    vector<uint8_t> bytes;
    bytes.reserve(tvec3::length() * sizeof(tfloat) * vec.size());

    for (const auto &v : vec)
    {
        append(bytes, v.x);
        append(bytes, v.y);
        append(bytes, v.z);
    }

    return bytes;
}

vector<tvec3> Primitive::uint8_to_vec(const vector<uint8_t> &bytes) const
{
    vector<tvec3> vec;
    vec.resize(bytes.size() / (tvec3::length() * sizeof(tfloat)));
    size_t fls = sizeof(tfloat);
    size_t shift = fls * tvec3::length();

    for (size_t i = 0, j = 0; i < bytes.size(); i += shift, ++j)
    {
        memcpy(&vec[j].x, &bytes[i], fls);
        memcpy(&vec[j].y, &bytes[i + fls], fls);
        memcpy(&vec[j].z, &bytes[i + fls + fls], fls);
    }

    return vec;
}

string Primitive::vec_to_string(const vector<tvec3> &vec) const
{
    vector<uint8_t> ui8 = vec_to_unit8(vec);
    using base64 = cppcodec::base64_rfc4648;
    return base64::encode(&ui8[0], ui8.size());
}

vector<tvec3> Primitive::string_to_vec(const string &s) const
{
    using base64 = cppcodec::base64_rfc4648;
    const vector<uint8_t> ui8 = base64::decode(s);
    return uint8_to_vec(ui8);
}

void Primitive::push_vert(const tvec3 &vec)
{
    vertices.emplace_back(vec);
}
void Primitive::push_vert(const tvec3 &vec1, const tvec3 &vec2)
{
    vertices.emplace_back(vec1);
    vertices.emplace_back(vec2);
}
void Primitive::push_vert(const tvec3 &vec1, const tvec3 &vec2, const tvec3 &vec3)
{
    vertices.insert(vertices.end(), {vec1, vec2, vec3});
}

void Primitive::deserialize(const json data)
{
    const auto sverts = data.at("vertices").get<string>();
    vertices = string_to_vec(sverts);
    data.at("tags").get_to(tags);
}

json Primitive::serialize() const
{
    return {
        {"vertices", vec_to_string(vertices)},
        {"tags", tags},
        {"type", type()}};
}

size_t pair_hash::operator()(const pair<int, int> &p) const
{
    auto h1 = hash<int>{}(p.first);
    auto h2 = hash<int>{}(p.second);

    // Mainly for demonstration purposes, i.e. works but is overly simple
    // In the real world, use sth. like boost.hash_combine
    return h1 ^ h2;
}