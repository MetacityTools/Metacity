#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "json/pybind11_json.hpp"
#include <filesystem>
#include "models.hpp"
#include "loaders.hpp"
#include "points.hpp"
#include "segments.hpp"
#include "mesh.hpp"
#include "legobuilder.hpp"

namespace py = pybind11;
using jsonref = const json;

class PyBaseModel : public BaseModel {
public:
    /* Inherit the constructors */
    ///Base Model Base model constructor
    using BaseModel::BaseModel;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE_PURE(
            const char *,/* Return type */
            BaseModel,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }
};

class PyLoaderModel : public ModelLoader {
public:
    /* Inherit the constructors */
    using ModelLoader::ModelLoader;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE_PURE(
            const char *,/* Return type */
            BaseModel,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> transform() const override {
        PYBIND11_OVERRIDE_PURE(
            shared_ptr<Model>,/* Return type */
            BaseModel,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }
};

class PyModel : public Model {
public:
    /* Inherit the constructors */
    using Model::Model;

    /* Trampoline (need one for each virtual function) */
    virtual json serialize() const override {
        PYBIND11_OVERRIDE(
            json,/* Return type */
            Model,/* Parent class */
            serialize,/* Name of function in C++ (must match Python name) */
                      /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void deserialize(jsonref data) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            Model,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE_PURE(
            const char *,/* Return type */
            Model,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> copy() const override {
        PYBIND11_OVERRIDE_PURE(
            shared_ptr<Model>,/* Return type */
            Model,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE_PURE(
            size_t,/* Return type */
            Model,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void add_attribute(const string & name, const uint32_t value) override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
            Model,/* Parent class */
            add_attribute,/* Name of function in C++ (must match Python name) */
            name, value/* Argument(s) */
        );
    }
};


/**
*   Python binding class, wrapper for MultiPoint.
*/

class PyMultiPoint : public MultiPoint {
public:
    /* Inherit the constructors */
    using MultiPoint::MultiPoint;

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> transform() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            MultiPoint,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            MultiPoint,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }
};


class PyPoints : public Points {
public:
    /* Inherit the constructors */
    using Points::Points;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            Points,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> copy() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            Points,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE(
            size_t,/* Return type */
            Points,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void add_attribute(const string & name, const uint32_t value) override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
            Points,/* Parent class */
            add_attribute,/* Name of function in C++ (must match Python name) */
            name, value/* Argument(s) */
        );
    }
};



class PyMultiLine : public MultiLine {
public:
    /* Inherit the constructors */
    using MultiLine::MultiLine;

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> transform() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            MultiLine,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            MultiLine,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }
};

class PySegments : public Segments {
public:
    /* Inherit the constructors */
    using Segments::Segments;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            Segments,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> copy() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            Segments,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE(
            size_t,/* Return type */
            Segments,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void add_attribute(const string & name, const uint32_t value) override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
            Segments,/* Parent class */
            add_attribute,/* Name of function in C++ (must match Python name) */
            name, value/* Argument(s) */
        );
    }
};

class PyMultiPolygon : public MultiPolygon {
public:
    /* Inherit the constructors */
    using MultiPolygon::MultiPolygon;


    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> transform() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            MultiPolygon,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            MultiPolygon,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }
};

class PyMesh : public Mesh {
public:
    /* Inherit the constructors */
    using Mesh::Mesh;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            Mesh,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> copy() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            Mesh,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE(
            size_t,/* Return type */
            Mesh,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void add_attribute(const string & name, const uint32_t value) override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
            Mesh,/* Parent class */
            add_attribute,/* Name of function in C++ (must match Python name) */
            name, value/* Argument(s) */
        );
    }
};


PYBIND11_MODULE(geometry, m) {
    py::class_<BaseModel, std::shared_ptr<BaseModel>, PyBaseModel>(m, "BaseModel")
        .def(py::init<>(), "Base model constructor")
        .def_property_readonly("type", &BaseModel::type)
        .def_property_readonly("tags", &BaseModel::get_tags)
        .def("add_tag", &BaseModel::add_tag)
        .doc() = "Doc test base model";


    py::class_<ModelLoader, std::shared_ptr<ModelLoader>, PyLoaderModel>(m, "ModelLoader")
        .def(py::init<>())
        .def_property_readonly("type", &ModelLoader::type)
        .def("transform", &ModelLoader::transform);


    py::class_<MultiPoint, std::shared_ptr<MultiPoint>, BaseModel, PyMultiPoint>(m, "MultiPoint")
        .def(py::init<>())
        .def_property_readonly("type", &MultiPoint::type)
        .def("push_p2", &MultiPoint::push_p2)
        .def("push_p3", &MultiPoint::push_p3)
        .def("transform", &MultiPoint::transform);


    py::class_<MultiLine, std::shared_ptr<MultiLine>, BaseModel, PyMultiLine>(m, "MultiLine")
        .def(py::init<>())
        .def_property_readonly("type", &MultiLine::type)
        .def("push_l2", &MultiLine::push_l2)
        .def("push_l3", &MultiLine::push_l3)
        .def("transform", &MultiLine::transform);


    py::class_<MultiPolygon, std::shared_ptr<MultiPolygon>, BaseModel, PyMultiPolygon>(m, "MultiPolygon")
        .def(py::init<>())
        .def_property_readonly("type", &MultiPolygon::type)
        .def("push_p2", &MultiPolygon::push_p2)
        .def("push_p3", &MultiPolygon::push_p3)
        .def("transform", &MultiPolygon::transform);


    py::class_<Model, std::shared_ptr<Model>, BaseModel, PyModel>(m, "Model")
        .def(py::init<>())
        .def_property_readonly("type", &Model::type)
        .def_property_readonly("centroid", &Model::centroid)
        .def_property_readonly("bounding_box", &Model::bounding_box)
        .def("shift", &Model::shift)
        .def("add_attribute", py::overload_cast<const string &, const uint32_t>(&Model::add_attribute))
        .def("copy", &Model::copy)
        .def("to_obj", &Model::to_obj)
        .def("serialize", &Model::serialize)
        .def("deserialize", &Model::deserialize);


    py::class_<Points, std::shared_ptr<Points>, Model, PyPoints>(m, "Points")
        .def(py::init<>())
        .def_property_readonly("type", &Points::type)
        .def("copy", &Points::copy)
        .def("to_obj", &Points::to_obj);


    py::class_<Segments, std::shared_ptr<Segments>, Model, PySegments>(m, "Segments")
        .def(py::init<>())
        .def_property_readonly("type", &Segments::type)
        .def("add_attribute", py::overload_cast<const string &, const uint32_t>(&Segments::add_attribute))
        .def("copy", &Segments::copy)
        .def("to_obj", &Segments::to_obj);


    py::class_<Mesh, std::shared_ptr<Mesh>, Model, PyMesh>(m, "Mesh")
        .def(py::init<>())
        .def_property_readonly("type", &Mesh::type)
        .def("copy", &Mesh::copy)
        .def("to_obj", &Mesh::to_obj);
        

    py::class_<LegoBuilder, std::shared_ptr<LegoBuilder>>(m, "LegoBuilder")
        .def(py::init<>())
        .def("insert_model", &LegoBuilder::insert_model)
        .def("build_heightmap", &LegoBuilder::build_heightmap)
        .def("legofy", &LegoBuilder::legofy)
        .def("lego_to_png", &LegoBuilder::lego_to_png);
}
