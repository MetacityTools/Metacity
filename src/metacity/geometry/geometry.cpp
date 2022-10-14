#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "deps/gltf/pybind11_json.hpp"
#include "progress.hpp"
#include "mesh/model.hpp"
#include "mesh/attribute.hpp"
#include "mesh/layer.hpp"
#include "mesh/grid.hpp"
#include "mesh/quadtree.hpp"

#define TINYGLTF_IMPLEMENTATION
#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "deps/gltf/tiny_gltf.h"

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
        .def("push_polygon3D", &Attribute::push_polygon3D)
        .def_property_readonly("geom_type", &Attribute::geom_type);

    py::class_<Model, std::shared_ptr<Model>>(m, "Model")
        .def(py::init<>())
        .def("add_attribute", &Model::add_attribute)
        .def("get_attribute", &Model::get_attribute)
        .def("set_metadata", &Model::set_metadata)
        .def_property_readonly("metadata", &Model::get_metadata)
        .def("attribute_exists", &Model::attribute_exists)
        .def_property_readonly("geom_type", &Model::geom_type);

    py::class_<Layer, std::shared_ptr<Layer>>(m, "Layer")
        .def(py::init<>())
        .def("add_model", &Layer::add_model)
        .def("add_models", &Layer::add_models)
        .def("get_models", &Layer::get_models)
        .def("to_gltf", &Layer::to_gltf)
        .def("from_gltf", &Layer::from_gltf)
        .def("map_to_height", &Layer::map_to_height)
        .def("simplify_envelope", &Layer::simplify_envelope)
        .def("simplify_remesh_height", &Layer::simplify_remesh_height)
        .def("move_to_plane_z", &Layer::move_to_plane_z)
        .def_property_readonly("size", &Layer::size);

    py::class_<Grid, std::shared_ptr<Grid>>(m, "Grid")
        .def(py::init<tfloat, tfloat>())
        .def("add_layer", &Grid::add_layer)
        .def("add_model", &Grid::add_model)
        .def("tile_merge", &Grid::tile_merge)
        .def("to_gltf", &Grid::to_gltf);

    py::class_<Progress, std::shared_ptr<Progress>>(m, "Progress")
        .def(py::init<string>())
        .def("update", &Progress::update);

    py::class_<QuadTree, std::shared_ptr<QuadTree>>(m, "QuadTree")
        .def(py::init<const vector<shared_ptr<Model>> &, size_t>())
        .def(py::init<shared_ptr<Layer>, size_t>())
        .def("merge_at_level", &QuadTree::merge_at_level)
        .def("to_json", &QuadTree::to_json, py::arg("dirname"), py::arg("yield_models_at_level"), py::arg("store_metadata") = true);
}
