#include <stdexcept>
#include <numeric>
#include "model.hpp"
#include "triangulation.hpp"
#include "cppcodec/base64_rfc4648.hpp"
#include "gltf/tiny_gltf.h"

//===============================================================================
Model::Model() {}

void Model::add_attribute(const string &name, shared_ptr<Attribute> attribute) {
    if (attrib.find(name) != attrib.end()) {
        throw runtime_error("Attribute already exists");
    }
    attrib[name] = attribute;
}

shared_ptr<Attribute> Model::get_attribute(const string &name) {
    if (attrib.find(name) == attrib.end()) {
        throw runtime_error("Attribute does not exist");
    }
    return attrib[name];
}

bool Model::attribute_exists(const string &name) {
    return attrib.find(name) != attrib.end();
}

void Model::to_gltf(tinygltf::Model & model)
{
    int mesh_index;
    to_gltf_mesh(model, mesh_index);
    to_gltf_scene(model, mesh_index);
}

void Model::to_gltf_scene(tinygltf::Model & model, const int mesh_index)
{
    if (model.scenes.size() == 0) {
        tinygltf::Scene scene;
        model.scenes.push_back(scene);
    }

    int node_index;
    to_gltf_node(model, mesh_index, node_index);
    model.scenes[0].nodes.push_back(node_index);
}

void Model::to_gltf_node(tinygltf::Model & model, const int mesh_index, int & node_index)
{
    tinygltf::Node node;
    node.mesh = mesh_index;
    model.nodes.push_back(node);
    node_index = model.nodes.size() - 1;
}

void Model::to_gltf_mesh(tinygltf::Model & model, int & mesh_index)
{
    tinygltf::Mesh mesh;
    to_gltf_primitive(model, mesh);
    model.meshes.push_back(mesh);
    mesh_index = model.meshes.size() - 1;
}

void Model::to_gltf_primitive(tinygltf::Model & model, tinygltf::Mesh & mesh)
{
    tinygltf::Primitive primitive;
    to_gltf_attribute(model, primitive, "POSITION");
    mesh.primitives.push_back(primitive);
}

void Model::to_gltf_attribute(tinygltf::Model & model, tinygltf::Primitive & primitive, const string &name)
{
    int accessor_index, mode;
    shared_ptr<Attribute> position_attribute = get_attribute(name);
    position_attribute->to_gltf(model, mode, accessor_index);
    primitive.mode = mode;
    primitive.indices = -1; //no indices
    primitive.attributes[name] = accessor_index;
}

//===============================================================================


void Model::from_gltf(const tinygltf::Model & model, const int mesh_index)
{
    mesh_validity_check(model, mesh_index);
    const tinygltf::Mesh & mesh = model.meshes[mesh_index];
    const tinygltf::Primitive & primitive = mesh.primitives[0];
    from_gltf_attribute(model, primitive, "POSITION");
}

void Model::from_gltf_attribute(const tinygltf::Model & model, const tinygltf::Primitive & primitive, const string &name)
{
    if (primitive.attributes.find(name) == primitive.attributes.end()) {
        throw runtime_error("Attribute does not exist");
    }

    int attribute_index = primitive.attributes.at(name);
    shared_ptr<Attribute> attribute = make_shared<Attribute>();
    attribute->from_gltf(model, attribute_index);
    add_attribute(name, attribute);
}


//===============================================================================
// Checks

void Model::mesh_validity_check(const tinygltf::Model & model, const int mesh_index)
{
    if (mesh_index >= model.meshes.size()) {
        throw runtime_error("Mesh index out of range");
    }

    if (model.meshes[mesh_index].primitives.size() != 1) {
        throw runtime_error("Only one primitive per mesh is supported");
    }

    if (model.meshes[mesh_index].primitives[0].indices != -1) {
        throw runtime_error("Indices are not supported");
    }

    if (model.meshes[mesh_index].primitives[0].attributes.size() != 1) {
        throw runtime_error("Only one attribute per primitive is supported");
    }
}

