#pragma once
#include <vector>
#include "types.hpp"
#include "gltf/tiny_gltf.h"

using namespace std;


enum AttributeType {
    NONE,
    POINT,
    SEGMENT,
    POLYGON
};


class Attribute {
public:
    Attribute();
    void push_point2D(const vector<tfloat> & ivertices);
    void push_point3D(const vector<tfloat> & ivertices);
    void push_line2D(const vector<tfloat> & ivertices);
    void push_line3D(const vector<tfloat> & ivertices); 
    void push_polygon2D(const vector<vector<tfloat>> & ivertices);
    void push_polygon3D(const vector<vector<tfloat>> & ivertices); 
    void to_gltf(tinygltf::Model & model, int & mode, int & accessor_index) const;
    void from_gltf(const tinygltf::Model & model, const int mode, const int accessor_index);
    tvec3 sum() const;
    size_t size() const;

protected:
    tvec3 vmin() const;
    tvec3 vmax() const;

    int  get_gltf_mode() const;
    void set_gltf_mode(int mode);
    void to_gltf_buffer(tinygltf::Model & model, int & buffer_index, int & size) const;
    void to_gltf_buffer_view(tinygltf::Model & model, const int buffer_index, const int size, int & buffer_view_index) const;
    void to_gltf_accessor(tinygltf::Model & model, const int buffer_view_index, int & accessor_index) const;

    void allowedAttributeType(AttributeType type);
    void attr_type_check(const tinygltf::Model & model, const int attribute_index) const;

    vector<tvec3> data;
    AttributeType type;
};


