#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "deps/gltf/pybind11_json.hpp"
#include "progress.hpp"
#include "mesh_pipeline/model.hpp"
#include "mesh_pipeline/attribute.hpp"
#include "mesh_pipeline/layer.hpp"
#include "mesh_pipeline/grid.hpp"
#include "vector_pipeline/graph.hpp"

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

    py::class_<Edge, std::shared_ptr<Edge>>(m, "Edge")
        .def(py::init<size_t, size_t, size_t, std::shared_ptr<Attribute>, nlohmann::json>());

    py::class_<Node, std::shared_ptr<Node>>(m, "Node")
        .def(py::init<size_t, tfloat, tfloat, nlohmann::json>());

    py::class_<Graph, std::shared_ptr<Graph>>(m, "Graph")
        .def(py::init<>())
        .def("add_node", &Graph::add_node)
        .def("add_edge", &Graph::add_edge)
        .def_property_readonly("node_count", &Graph::get_node_count)
        .def_property_readonly("edge_count", &Graph::get_edge_count);
}
