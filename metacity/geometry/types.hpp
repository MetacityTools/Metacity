#pragma once
#include "glm/glm.hpp"
#include "cppcodec/base64_rfc4648.hpp"
#include "json/json.hpp"
#include <vector>
#include <iostream>

using tvec3 = glm::highp_f64vec3;
using tvec2 = glm::highp_f64vec2;
using tfloat = double;
using json = nlohmann::json;

using namespace std;

ostream &operator<<(ostream &os, const tvec3 &vec);
ostream &operator<<(ostream &os, const vector<tvec3> &vec);


using Polygon = vector<vector<tvec3>>;
using Polygons = vector<vector<vector<tvec3>>>;

// fully defined
void grid_coords(const tvec3 &point, const tfloat tile_size, pair<int, int> &coords);

vector<tfloat> vec_to_tfloat(const vector<tvec3> &vec);
vector<uint8_t> vec_to_uint8(const vector<tvec3> &vec);
vector<tvec3> uint8_to_vec(const vector<uint8_t> &bytes);
string vec_to_string(const vector<tvec3> &vec);
vector<tvec3> string_to_vec(const string &s);

struct pair_hash
{
    size_t operator()(const pair<int, int> &p) const;
};

//===============================================================================
// templates
template <typename T>
void append(vector<uint8_t> &vec, T f)
{
    uint8_t *d = (uint8_t *)&f;
    vec.insert(vec.end(), d, d + sizeof(T));
};

template <typename T>
vector<uint8_t> T_to_uint8(const vector<T> &vec)
{
    vector<uint8_t> bytes;
    bytes.reserve(sizeof(T) * vec.size());

    for (const auto &v : vec)
        append(bytes, v);

    return bytes;
};

template <typename T>
vector<T> uint8_to_T(const vector<uint8_t> &bytes)
{
    vector<T> vec;
    vec.resize(bytes.size() / (sizeof(T)));
    size_t tls = sizeof(T);

    for (size_t i = 0, j = 0; i < bytes.size(); i += tls, ++j)
        memcpy(&vec[j], &bytes[i], tls);

    return vec;
};

template <typename T>
string T_to_string(const vector<T> &vec)
{
    vector<uint8_t> ui8 = T_to_uint8<T>(vec);
    using base64 = cppcodec::base64_rfc4648;
    return base64::encode(&ui8[0], ui8.size());
};

template <typename T>
vector<T> string_to_T(const string &s)
{
    using base64 = cppcodec::base64_rfc4648;
    const vector<uint8_t> ui8 = base64::decode(s);
    return uint8_to_T<T>(ui8);
};