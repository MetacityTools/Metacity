#include <stdexcept>
#include <numeric>
#include "models.hpp"
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


