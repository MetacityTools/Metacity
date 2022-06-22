#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <filesystem>
#include "model.hpp"
#include "attribute.hpp"
#include "layer.hpp"

#define TINYGLTF_IMPLEMENTATION
#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "gltf/tiny_gltf.h"

namespace py = pybind11;
using namespace std;


PYBIND11_MODULE(geometry, m) {
    py::class_<Attribute, std::shared_ptr<Attribute>>(m, "Attribute")
        .def(py::init<>())
        .def("push_point2D", &Attribute::push_point2D)
        .def("push_point3D", &Attribute::push_point3D)
        .def("push_line2D", &Attribute::push_line2D)
        .def("push_line3D", &Attribute::push_line3D)
        .def("push_polygon2D", &Attribute::push_polygon2D)
        .def("push_polygon3D", &Attribute::push_polygon3D);

    py::class_<Model, std::shared_ptr<Model>>(m, "Model")
        .def(py::init<>())
        .def("add_attribute", &Model::add_attribute)
        .def("get_attribute", &Model::get_attribute)
        .def("attribute_exists", &Model::attribute_exists);

    py::class_<Layer, std::shared_ptr<Layer>>(m, "Layer")
        .def(py::init<>())
        .def("add_model", &Layer::add_model)
        .def("add_models", &Layer::add_models)
        .def("get_models", &Layer::get_models)
        .def("to_gltf", &Layer::to_gltf)
        .def("from_gltf", &Layer::from_gltf);

}
