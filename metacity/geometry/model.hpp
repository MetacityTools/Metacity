#pragma once
#include <vector>
#include <unordered_map>
#include "types.hpp"
#include "attribute.hpp"

using namespace std;


class Model
{
public:
    Model();
    void add_attribute(const string &name, shared_ptr<Attribute> attribute);
    shared_ptr<Attribute> get_attribute(const string &name);
    bool attribute_exists(const string &name);
    void to_gltf(tinygltf::Model & model);
    void from_gltf(const tinygltf::Model & model, const int mesh_index);
protected:
    void to_gltf_attribute(tinygltf::Model & model, tinygltf::Primitive & primitive, const string &name);
    void to_gltf_scene(tinygltf::Model & model, const int mesh_index);
    void to_gltf_node(tinygltf::Model & model, const int mesh_index, int & node_index);
    void to_gltf_mesh(tinygltf::Model & model, int & mesh_index);
    void to_gltf_primitive(tinygltf::Model & model, tinygltf::Mesh & mesh);
    void to_gltf_scene(tinygltf::Model & model, tinygltf::Scene & scene);

    void from_gltf_attribute(const tinygltf::Model & model, const tinygltf::Primitive & primitive, const string &name);

    void mesh_validity_check(const tinygltf::Model & model, const int mesh_index);
    void attr_validity_check(const tinygltf::Model & model, const int attribute_index);
    unordered_map<string, shared_ptr<Attribute>> attrib;
    //TODO metadata?

};

