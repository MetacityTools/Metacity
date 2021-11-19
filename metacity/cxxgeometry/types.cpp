#include "types.hpp"

void grid_coords(const tvec3 &point, const tfloat tile_size, pair<int, int> &coords)
{
    coords.first = (point.x / tile_size);
    coords.second = (point.y / tile_size);
}

vector<tfloat> vec_to_tfloat(const vector<tvec3> &vec)
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

vector<uint8_t> vec_to_unit8(const vector<tvec3> &vec)
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

vector<uint8_t> vec_to_f_to_uint8(const vector<tvec3> &vec)
{
    vector<uint8_t> bytes;
    bytes.reserve(tvec3::length() * sizeof(float_t) * vec.size());

    for (const auto &v : vec)
    {
        append(bytes, (float_t) v.x);
        append(bytes, (float_t) v.y);
        append(bytes, (float_t) v.z);
    }

    return bytes;
}

vector<tvec3> uint8_to_vec(const vector<uint8_t> &bytes)
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

vector<tvec3> uint8_to_vec2_to_vec3(const vector<uint8_t> &bytes)
{
    vector<tvec3> vec;
    vec.resize(bytes.size() / (tvec2::length() * sizeof(tfloat)));
    size_t fls = sizeof(tfloat);
    size_t shift = fls * tvec2::length();

    for (size_t i = 0, j = 0; i < bytes.size(); i += shift, ++j)
    {
        memcpy(&vec[j].x, &bytes[i], fls);
        memcpy(&vec[j].y, &bytes[i + fls], fls);
        vec[j].z = 0;
    }

    return vec;
}

string vec_to_string(const vector<tvec3> &vec)
{
    vector<uint8_t> ui8 = vec_to_unit8(vec);
    using base64 = cppcodec::base64_rfc4648;
    return base64::encode(&ui8[0], ui8.size());
}

string vec_to_f_to_string(const vector<tvec3> &vec)
{
    vector<uint8_t> ui8 = vec_to_f_to_uint8(vec);
    using base64 = cppcodec::base64_rfc4648;
    return base64::encode(&ui8[0], ui8.size());
}

vector<tvec3> string_to_vec(const string &s) 
{
    using base64 = cppcodec::base64_rfc4648;
    const vector<uint8_t> ui8 = base64::decode(s);
    return uint8_to_vec(ui8);
}

vector<tvec3> string_to_vec2_to_vec3(const string &s) 
{
    using base64 = cppcodec::base64_rfc4648;
    const vector<uint8_t> ui8 = base64::decode(s);
    return uint8_to_vec2_to_vec3(ui8);
}

size_t pair_hash::operator()(const pair<int, int> &p) const
{
    auto h1 = hash<int>{}(p.first);
    auto h2 = hash<int>{}(p.second);

    // Mainly for demonstration purposes, i.e. works but is overly simple
    // In the real world, use sth. like boost.hash_combine
    return h1 ^ h2;
}

ostream &operator<<(ostream &os, const tvec3 &vec)
{
    os << vec.x << " " << vec.y << " " << vec.z;
    return os;
}

ostream &operator<<(ostream &os, const vector<tvec3> &vec)
{
    os << "[\n";
    for (const auto &v : vec)
        os << "   " << v << "\n";
    os << "]";
    return os;
}
