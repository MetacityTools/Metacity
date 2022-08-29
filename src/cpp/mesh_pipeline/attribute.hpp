#pragma once
#include <vector>
#include "../types.hpp"
#include "../deps/gltf/tiny_gltf.h"

using namespace std;

enum class AttributeType : uint8_t
{
    NONE = 0,
    POINT,
    SEGMENT,
    TRIANGLE,
};

inline int to_number(AttributeType type)
{
    return static_cast<int>(type);
}

class Attribute
{
public:
    Attribute();
    void push_point2D(const vector<tfloat> &ivertices);
    void push_point3D(const vector<tfloat> &ivertices);
    void push_line2D(const vector<tfloat> &ivertices);
    void push_line3D(const vector<tfloat> &ivertices);
    void push_polygon2D(const vector<vector<tfloat>> &ivertices);
    void push_polygon3D(const vector<vector<tfloat>> &ivertices);
    void push_triangles(const vector<tvec3> &ivertices);

    AttributeType type() const;
    void to_gltf(tinygltf::Model &model, AttributeType &type, int &accessor_index) const;
    void from_gltf(const tinygltf::Model &model, AttributeType type, const int accessor_index);

    tvec3 sum() const;
    size_t size() const;

    shared_ptr<Attribute> clone() const;

    void merge(shared_ptr<Attribute> attribute);

    tvec3 &operator[](const size_t index);
    const tvec3 &operator[](const size_t index) const;

    pair<tvec3, tvec3> bbox() const;
    AttributeType geom_type() const;

protected:
    tvec3 vmin() const;
    tvec3 vmax() const;

    void to_gltf_buffer(tinygltf::Model &model, int &buffer_index, int &size) const;
    void to_gltf_buffer_view(tinygltf::Model &model, const int buffer_index, const int size, int &buffer_view_index) const;
    void to_gltf_accessor(tinygltf::Model &model, const int buffer_view_index, int &accessor_index) const;

    void allowedAttributeType(AttributeType type);
    void attr_type_check(const tinygltf::Model &model, const int attribute_index) const;

    vector<tvec3> data;
    AttributeType dtype;
};
