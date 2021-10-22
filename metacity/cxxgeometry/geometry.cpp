#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "json/pybind11_json.hpp"
#include <filesystem>
#include "primitives.hpp"
#include "points.hpp"
#include "lines.hpp"
#include "polygons.hpp"

namespace py = pybind11;
using jsonref = const json;


class PyPrimitive : public Primitive {
public:
    /* Inherit the constructors */
    using Primitive::Primitive;

    /* Trampoline (need one for each virtual function) */
    virtual json serialize() const override {
        PYBIND11_OVERRIDE(
            json,/* Return type */
            Primitive,/* Parent class */
            serialize,/* Name of function in C++ (must match Python name) */
                      /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void deserialize(jsonref data) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            Primitive,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<SimplePrimitive> transform() const override {
        PYBIND11_OVERRIDE_PURE(
            shared_ptr<SimplePrimitive>,/* Return type */
            Primitive,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE_PURE(
            const char *,/* Return type */
            Primitive,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }
};

class PySimplePrimitive : public SimplePrimitive {
public:
    /* Inherit the constructors */
    using SimplePrimitive::SimplePrimitive;

    /* Trampoline (need one for each virtual function) */
    virtual json serialize() const override {
        PYBIND11_OVERRIDE(
            json,/* Return type */
            SimplePrimitive,/* Parent class */
            serialize,/* Name of function in C++ (must match Python name) */
                      /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void deserialize(jsonref data) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            SimplePrimitive,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<SimplePrimitive> transform() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<SimplePrimitive>,/* Return type */
            SimplePrimitive,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE_PURE(
            const char *,/* Return type */
            SimplePrimitive,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<SimplePrimitive>> slice_to_grid(const tfloat tile_size) const override {
        PYBIND11_OVERRIDE_PURE(
            vector<shared_ptr<SimplePrimitive>>,/* Return type */
            SimplePrimitive,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<SimplePrimitive> copy() const override {
        PYBIND11_OVERRIDE_PURE(
            shared_ptr<SimplePrimitive>,/* Return type */
            SimplePrimitive,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void map(const shared_ptr<SimpleMultiPolygon> target) override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
            SimplePrimitive,/* Parent class */
            map,/* Name of function in C++ (must match Python name) */
            target/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE_PURE(
            size_t,/* Return type */
            SimplePrimitive,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
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
            MultiPoint,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<SimplePrimitive> transform() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<SimplePrimitive>,/* Return type */
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

class PySimpleMultiPoint : public SimpleMultiPoint {
public:
    /* Inherit the constructors */
    using SimpleMultiPoint::SimpleMultiPoint;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            SimpleMultiPoint,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<SimplePrimitive>> slice_to_grid(const tfloat tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<SimplePrimitive>>,/* Return type */
            SimpleMultiPoint,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<SimplePrimitive> copy() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<SimplePrimitive>,/* Return type */
            SimpleMultiPoint,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void map(const shared_ptr<SimpleMultiPolygon> target) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            SimpleMultiPoint,/* Parent class */
            map,/* Name of function in C++ (must match Python name) */
            target/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE(
            size_t,/* Return type */
            SimpleMultiPoint,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
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
            MultiLine,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<SimplePrimitive> transform() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<SimplePrimitive>,/* Return type */
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

class PySimpleMultiLine : public SimpleMultiLine {
public:
    /* Inherit the constructors */
    using SimpleMultiLine::SimpleMultiLine;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            SimpleMultiLine,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<SimplePrimitive>> slice_to_grid(const tfloat tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<SimplePrimitive>>,/* Return type */
            SimpleMultiLine,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<SimplePrimitive> copy() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<SimplePrimitive>,/* Return type */
            SimpleMultiLine,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void map(const shared_ptr<SimpleMultiPolygon> target) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            SimpleMultiLine,/* Parent class */
            map,/* Name of function in C++ (must match Python name) */
            target/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE(
            size_t,/* Return type */
            SimpleMultiLine,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
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

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<SimplePrimitive> transform() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<SimplePrimitive>,/* Return type */
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

class PySimpleMultiPolygon : public SimpleMultiPolygon {
public:
    /* Inherit the constructors */
    using SimpleMultiPolygon::SimpleMultiPolygon;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            SimpleMultiPolygon,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<SimplePrimitive>> slice_to_grid(const tfloat tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<SimplePrimitive>>,/* Return type */
            SimpleMultiPolygon,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<SimplePrimitive> copy() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<SimplePrimitive>,/* Return type */
            SimpleMultiPolygon,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void map(const shared_ptr<SimpleMultiPolygon> target) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            SimpleMultiPolygon,/* Parent class */
            map,/* Name of function in C++ (must match Python name) */
            target/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE(
            size_t,/* Return type */
            SimpleMultiPolygon,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
        );
    }
};

PYBIND11_MODULE(geometry, m) {
    py::class_<Primitive, std::shared_ptr<Primitive>, PyPrimitive>(m, "Primitive")
        .def(py::init<>())
        .def_property_readonly("type", &Primitive::type)
        .def("transform", &Primitive::transform)
        .def("serialize", &Primitive::serialize)
        .def("deserialize", &Primitive::deserialize);


    py::class_<SimplePrimitive, std::shared_ptr<SimplePrimitive>, Primitive, PySimplePrimitive>(m, "SimplePrimitive")
        .def(py::init<>())
        .def_property_readonly("type", &SimplePrimitive::type)
        .def_property_readonly("centroid", &SimplePrimitive::centroid)
        .def_property_readonly("bounding_box", &SimplePrimitive::bounding_box)
        .def("shift", &SimplePrimitive::shift)
        .def("add_attribute", py::overload_cast<const string &, const uint32_t>(&SimplePrimitive::add_attribute))
        .def("slice_to_grid", &SimplePrimitive::slice_to_grid)
        .def("join", &SimplePrimitive::join)
        .def("copy", &SimplePrimitive::copy)
        .def("to_obj", &SimplePrimitive::to_obj)
        .def("map", &SimplePrimitive::map)
        .def("transform", &SimplePrimitive::transform)
        .def("serialize", &SimplePrimitive::serialize)
        .def("deserialize", &SimplePrimitive::deserialize);


    py::class_<MultiPoint, std::shared_ptr<MultiPoint>, Primitive, PyMultiPoint>(m, "MultiPoint")
        .def(py::init<>())
        .def_property_readonly("type", &MultiPoint::type)
        .def("push_p2", &MultiPoint::push_p2)
        .def("push_p3", &MultiPoint::push_p3)
        .def("transform", &MultiPoint::transform)
        .def("serialize", &MultiPoint::serialize)
        .def("deserialize", &MultiPoint::deserialize);


    py::class_<SimpleMultiPoint, std::shared_ptr<SimpleMultiPoint>, SimplePrimitive, PySimpleMultiPoint>(m, "SimpleMultiPoint")
        .def(py::init<>())
        .def_property_readonly("type", &SimpleMultiPoint::type)
        .def("copy", &SimpleMultiPoint::copy)
        .def("to_obj", &SimpleMultiPoint::to_obj)
        .def("map", &SimpleMultiPoint::map)
        .def("slice_to_grid", &SimpleMultiPoint::slice_to_grid);


    py::class_<MultiLine, std::shared_ptr<MultiLine>, Primitive, PyMultiLine>(m, "MultiLine")
        .def(py::init<>())
        .def_property_readonly("type", &MultiLine::type)
        .def("push_l2", &MultiLine::push_l2)
        .def("push_l3", &MultiLine::push_l3)
        .def("transform", &MultiLine::transform)
        .def("serialize", &MultiLine::serialize)
        .def("deserialize", &MultiLine::deserialize);


    py::class_<SimpleMultiLine, std::shared_ptr<SimpleMultiLine>, SimplePrimitive, PySimpleMultiLine>(m, "SimpleMultiLine")
        .def(py::init<>())
        .def_property_readonly("type", &SimpleMultiLine::type)
        .def("copy", &SimpleMultiLine::copy)
        .def("to_obj", &SimpleMultiLine::to_obj)
        .def("map", &SimpleMultiLine::map)
        .def("slice_to_grid", &SimpleMultiLine::slice_to_grid);


    py::class_<MultiPolygon, std::shared_ptr<MultiPolygon>, Primitive, PyMultiPolygon>(m, "MultiPolygon")
        .def(py::init<>())
        .def_property_readonly("type", &MultiPolygon::type)
        .def("push_p2", &MultiPolygon::push_p2)
        .def("push_p3", &MultiPolygon::push_p3)
        .def("transform", &MultiPolygon::transform)
        .def("serialize", &MultiPolygon::serialize)
        .def("deserialize", &MultiPolygon::deserialize);


    py::class_<SimpleMultiPolygon, std::shared_ptr<SimpleMultiPolygon>, SimplePrimitive, PySimpleMultiPolygon>(m, "SimpleMultiPolygon")
        .def(py::init<>())
        .def_property_readonly("type", &SimpleMultiPolygon::type)
        .def("copy", &SimpleMultiPolygon::copy)
        .def("to_obj", &SimpleMultiPolygon::to_obj)
        .def("map", &SimpleMultiPolygon::map)
        .def("slice_to_grid", &SimpleMultiPolygon::slice_to_grid);
}