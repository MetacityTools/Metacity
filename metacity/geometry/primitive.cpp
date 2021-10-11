#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <filesystem>
#include "primitives.hpp"

namespace py = pybind11;
using jsonref = const json;

class PyPrimitive : public Primitive {
public:
    /* Inherit the constructors */
    using Primitive::Primitive;

    /* Trampoline (need one for each virtual function) */
    virtual json serialize() const override {
        PYBIND11_OVERRIDE_PURE(
            json,/* Return type */
            Primitive,/* Parent class */
            serialize,/* Name of function in C++ (must match Python name) */
                      /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void deserialize(jsonref data) override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
            Primitive,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
        );
    }
};

class PyMultiPoint : public MultiPoint {
public:
    /* Inherit the constructors */
    using MultiPoint::MultiPoint;

    /* Trampoline (need one for each virtual function) */
    virtual json serialize() const override {
        PYBIND11_OVERRIDE(
            json,/* Return type */
            MultiPoint,/* Parent class */
            serialize,/* Name of function in C++ (must match Python name) */
                      /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void deserialize(jsonref data) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            PyMultiPoint,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
        );
    }
};

class PyMultiLine : public MultiLine {
public:
    /* Inherit the constructors */
    using MultiLine::MultiLine;

    /* Trampoline (need one for each virtual function) */
    virtual json serialize() const override {
        PYBIND11_OVERRIDE(
            json,/* Return type */
            MultiLine,/* Parent class */
            serialize,/* Name of function in C++ (must match Python name) */
                      /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void deserialize(jsonref data) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            PyMultiLine,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
        );
    }
};

class PyMultiPolygon : public MultiPolygon {
public:
    /* Inherit the constructors */
    using MultiPolygon::MultiPolygon;

    /* Trampoline (need one for each virtual function) */
    virtual json serialize() const override {
        PYBIND11_OVERRIDE(
            json,/* Return type */
            MultiPolygon,/* Parent class */
            serialize,/* Name of function in C++ (must match Python name) */
                      /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void deserialize(jsonref data) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            MultiPolygon,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
        );
    }
};

PYBIND11_MODULE(primitive, m) {
    py::class_<Primitive, std::shared_ptr<Primitive>, PyPrimitive>(m, "Primitive")
        .def(py::init<>())
        .def_property_readonly("vertices", &Primitive::get_vertices)
        .def("serialize", &Primitive::serialize)
        .def("deserialize", &Primitive::deserialize);

    py::class_<MultiPoint, std::shared_ptr<MultiPoint>, Primitive, PyMultiPoint>(m, "MultiPoint")
        .def(py::init<>())
        .def("push_p2", &MultiPoint::push_p2)
        .def("push_p3", &MultiPoint::push_p3)
        .def("contents", &MultiPoint::contents)
        .def("serialize", &MultiPoint::serialize)
        .def("deserialize", &MultiPoint::deserialize);


    py::class_<MultiLine, std::shared_ptr<MultiLine>, Primitive, PyMultiLine>(m, "MultiLine")
        .def(py::init<>())
        .def("push_l2", &MultiLine::push_l2)
        .def("push_l3", &MultiLine::push_l3)
        .def("contents", &MultiLine::contents)
        .def("serialize", &MultiLine::serialize)
        .def("deserialize", &MultiLine::deserialize);


    py::class_<MultiPolygon, std::shared_ptr<MultiPolygon>, Primitive, PyMultiPolygon>(m, "MultiPolygon")
        .def(py::init<>())
        .def("push_p2", &MultiPolygon::push_p2)
        .def("push_p3", &MultiPolygon::push_p3)
        .def("contents", &MultiPolygon::contents)
        .def("serialize", &MultiPolygon::serialize)
        .def("triangulate", &MultiPolygon::triangulate)
        .def("deserialize", &MultiPolygon::deserialize);
}