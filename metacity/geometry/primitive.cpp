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
    virtual void transform() override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
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

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override {
        PYBIND11_OVERRIDE_PURE(
            vector<shared_ptr<Primitive>>,/* Return type */
            Primitive,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
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
    virtual void transform() override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
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

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<Primitive>>,/* Return type */
            MultiPoint,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }
};

class PySimpleMultiPoint : public SimpleMultiPoint {
public:
    /* Inherit the constructors */
    using SimpleMultiPoint::SimpleMultiPoint;

    /* Trampoline (need one for each virtual function) */
    virtual void transform() override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            SimpleMultiPoint,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

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
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<Primitive>>,/* Return type */
            SimpleMultiPoint,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
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
    virtual void transform() override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
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

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<Primitive>>,/* Return type */
            MultiLine,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }
};

class PySimpleMultiLine : public SimpleMultiLine {
public:
    /* Inherit the constructors */
    using SimpleMultiLine::SimpleMultiLine;

    /* Trampoline (need one for each virtual function) */
    virtual void transform() override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            SimpleMultiLine,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

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
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<Primitive>>,/* Return type */
            SimpleMultiLine,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
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
    virtual void transform() override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
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

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<Primitive>>,/* Return type */
            MultiPolygon,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }
};

class PySimpleMultiPolygon : public SimpleMultiPolygon {
public:
    /* Inherit the constructors */
    using SimpleMultiPolygon::SimpleMultiPolygon;

    /* Trampoline (need one for each virtual function) */
    virtual void transform() override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            SimpleMultiPolygon,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

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
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<Primitive>>,/* Return type */
            SimpleMultiPolygon,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }
};

PYBIND11_MODULE(primitive, m) {
    py::class_<Primitive, std::shared_ptr<Primitive>, PyPrimitive>(m, "Primitive")
        .def(py::init<>())
        .def_property_readonly("type", &Primitive::type)
        .def("slice_to_grid", &Primitive::slice_to_grid)
        .def("transform", &Primitive::transform)
        .def("serialize", &Primitive::serialize)
        .def("deserialize", &Primitive::deserialize);


    py::class_<MultiPoint, std::shared_ptr<MultiPoint>, Primitive, PyMultiPoint>(m, "MultiPoint")
        .def(py::init<>())
        .def_property_readonly("type", &MultiPoint::type)
        .def("slice_to_grid", &MultiPoint::slice_to_grid)
        .def("push_p2", &MultiPoint::push_p2)
        .def("push_p3", &MultiPoint::push_p3)
        .def("transform", &MultiPoint::transform)
        .def("contents", &MultiPoint::contents)
        .def("serialize", &MultiPoint::serialize)
        .def("deserialize", &MultiPoint::deserialize);


    py::class_<SimpleMultiPoint, std::shared_ptr<SimpleMultiPoint>, Primitive, PySimpleMultiPoint>(m, "SimpleMultiPoint")
        .def(py::init<const MultiPoint &>())
        .def_property_readonly("type", &SimpleMultiPoint::type)
        .def("slice_to_grid", &SimpleMultiPoint::slice_to_grid)
        .def("serialize", &SimpleMultiPoint::serialize)
        .def("deserialize", &SimpleMultiPoint::deserialize);


    py::class_<MultiLine, std::shared_ptr<MultiLine>, Primitive, PyMultiLine>(m, "MultiLine")
        .def(py::init<>())
        .def_property_readonly("type", &MultiLine::type)
        .def("slice_to_grid", &MultiLine::slice_to_grid)    
        .def("push_l2", &MultiLine::push_l2)
        .def("push_l3", &MultiLine::push_l3)
        .def("transform", &MultiLine::transform)
        .def("contents", &MultiLine::contents)
        .def("serialize", &MultiLine::serialize)
        .def("deserialize", &MultiLine::deserialize);


    py::class_<SimpleMultiLine, std::shared_ptr<SimpleMultiLine>, Primitive, PySimpleMultiLine>(m, "SimpleMultiLine")
        .def(py::init<const MultiLine &>())
        .def_property_readonly("type", &SimpleMultiLine::type)
        .def("slice_to_grid", &SimpleMultiLine::slice_to_grid)
        .def("serialize", &SimpleMultiLine::serialize)
        .def("deserialize", &SimpleMultiLine::deserialize);


    py::class_<MultiPolygon, std::shared_ptr<MultiPolygon>, Primitive, PyMultiPolygon>(m, "MultiPolygon")
        .def(py::init<>())
        .def_property_readonly("type", &MultiPolygon::type)
        .def("slice_to_grid", &MultiPolygon::slice_to_grid)
        .def("push_p2", &MultiPolygon::push_p2)
        .def("push_p3", &MultiPolygon::push_p3)
        .def("transform", &MultiPolygon::transform)
        .def("contents", &MultiPolygon::contents)
        .def("serialize", &MultiPolygon::serialize)
        .def("deserialize", &MultiPolygon::deserialize);


    py::class_<SimpleMultiPolygon, std::shared_ptr<SimpleMultiPolygon>, Primitive, PySimpleMultiPolygon>(m, "SimpleMultiPolygon")
        .def(py::init<const MultiPolygon &>())
        .def_property_readonly("type", &SimpleMultiPolygon::type)
        .def("slice_to_grid", &SimpleMultiPolygon::slice_to_grid)
        .def("serialize", &SimpleMultiPolygon::serialize)
        .def("deserialize", &SimpleMultiPolygon::deserialize);
}