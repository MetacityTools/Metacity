#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "json/pybind11_json.hpp"
#include <filesystem>
#include "models.hpp"
#include "points.hpp"
#include "lines.hpp"
#include "polygons.hpp"
#include "timepoints.hpp"
#include "legobuilder.hpp"
#include "interval.hpp"

namespace py = pybind11;
using jsonref = const json;


class PyBaseModel : public BaseModel {
public:
    /* Inherit the constructors */
    using BaseModel::BaseModel;

    /* Trampoline (need one for each virtual function) */
    virtual json serialize() const override {
        PYBIND11_OVERRIDE(
            json,/* Return type */
            BaseModel,/* Parent class */
            serialize,/* Name of function in C++ (must match Python name) */
                      /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void deserialize(jsonref data) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            BaseModel,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
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
    virtual shared_ptr<Model> transform() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            Model,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
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
    virtual vector<shared_ptr<Model>> slice_to_grid(const tfloat tile_size) const override {
        PYBIND11_OVERRIDE_PURE(
            vector<shared_ptr<Model>>,/* Return type */
            Model,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
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
    virtual void map(const shared_ptr<TriangularMesh> target) override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
            Model,/* Parent class */
            map,/* Name of function in C++ (must match Python name) */
            target/* Argument(s) */
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

class PyPointCloud : public PointCloud {
public:
    /* Inherit the constructors */
    using PointCloud::PointCloud;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            PointCloud,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<Model>> slice_to_grid(const tfloat tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<Model>>,/* Return type */
            PointCloud,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> copy() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            PointCloud,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void map(const shared_ptr<TriangularMesh> target) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            PointCloud,/* Parent class */
            map,/* Name of function in C++ (must match Python name) */
            target/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE(
            size_t,/* Return type */
            PointCloud,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void add_attribute(const string & name, const uint32_t value) override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
            PointCloud,/* Parent class */
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

class PySegmentCloud : public SegmentCloud {
public:
    /* Inherit the constructors */
    using SegmentCloud::SegmentCloud;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            SegmentCloud,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<Model>> slice_to_grid(const tfloat tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<Model>>,/* Return type */
            SegmentCloud,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> copy() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            SegmentCloud,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void map(const shared_ptr<TriangularMesh> target) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            SegmentCloud,/* Parent class */
            map,/* Name of function in C++ (must match Python name) */
            target/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE(
            size_t,/* Return type */
            SegmentCloud,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void add_attribute(const string & name, const uint32_t value) override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
            SegmentCloud,/* Parent class */
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

class PyTriangularMesh : public TriangularMesh {
public:
    /* Inherit the constructors */
    using TriangularMesh::TriangularMesh;

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            TriangularMesh,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual vector<shared_ptr<Model>> slice_to_grid(const tfloat tile_size) const override {
        PYBIND11_OVERRIDE(
            vector<shared_ptr<Model>>,/* Return type */
            TriangularMesh,/* Parent class */
            slice_to_grid,/* Name of function in C++ (must match Python name) */
            tile_size/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> copy() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            TriangularMesh,/* Parent class */
            copy,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void map(const shared_ptr<TriangularMesh> target) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            TriangularMesh,/* Parent class */
            map,/* Name of function in C++ (must match Python name) */
            target/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual size_t to_obj(const string & path, const size_t offset) const override {
        PYBIND11_OVERRIDE(
            size_t,/* Return type */
            TriangularMesh,/* Parent class */
            to_obj,/* Name of function in C++ (must match Python name) */
            path, offset/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void add_attribute(const string & name, const uint32_t value) override {
        PYBIND11_OVERRIDE_PURE(
            void,/* Return type */
            TriangularMesh,/* Parent class */
            add_attribute,/* Name of function in C++ (must match Python name) */
            name, value/* Argument(s) */
        );
    }
};

class PyMultiTimePoint : public MultiTimePoint {
public:
    /* Inherit the constructors */
    using MultiTimePoint::MultiTimePoint;

    /* Trampoline (need one for each virtual function) */
    virtual json serialize() const override {
        PYBIND11_OVERRIDE(
            json,/* Return type */
            MultiTimePoint,/* Parent class */
            serialize,/* Name of function in C++ (must match Python name) */
                      /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual void deserialize(jsonref data) override {
        PYBIND11_OVERRIDE(
            void,/* Return type */
            MultiTimePoint,/* Parent class */
            deserialize,/* Name of function in C++ (must match Python name) */
            data/* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual shared_ptr<Model> transform() const override {
        PYBIND11_OVERRIDE(
            shared_ptr<Model>,/* Return type */
            MultiTimePoint,/* Parent class */
            transform,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }

    /* Trampoline (need one for each virtual function) */
    virtual const char * type() const override {
        PYBIND11_OVERRIDE(
            const char *,/* Return type */
            MultiTimePoint,/* Parent class */
            type,/* Name of function in C++ (must match Python name) */
            /* Argument(s) */
        );
    }
};




PYBIND11_MODULE(geometry, m) {
    py::class_<BaseModel, std::shared_ptr<BaseModel>, PyBaseModel>(m, "BaseModel")
        .def(py::init<>())
        .def_property_readonly("type", &BaseModel::type)
        .def("transform", &BaseModel::transform)
        .def("serialize", &BaseModel::serialize)
        .def("deserialize", &BaseModel::deserialize);


    py::class_<Model, std::shared_ptr<Model>, BaseModel, PyModel>(m, "Model")
        .def(py::init<>())
        .def_property_readonly("type", &Model::type)
        .def_property_readonly("centroid", &Model::centroid)
        .def_property_readonly("bounding_box", &Model::bounding_box)
        .def("shift", &Model::shift)
        .def("add_attribute", py::overload_cast<const string &, const uint32_t>(&Model::add_attribute))
        .def("slice_to_grid", &Model::slice_to_grid)
        .def("join", &Model::join)
        .def("copy", &Model::copy)
        .def("to_obj", &Model::to_obj)
        .def("map", &Model::map)
        .def("transform", &Model::transform)
        .def("serialize", &Model::serialize)
        .def("serialize_stream", &Model::serialize_stream)
        .def("deserialize", &Model::deserialize);


    py::class_<MultiPoint, std::shared_ptr<MultiPoint>, BaseModel, PyMultiPoint>(m, "MultiPoint")
        .def(py::init<>())
        .def_property_readonly("type", &MultiPoint::type)
        .def("push_p2", &MultiPoint::push_p2)
        .def("push_p3", &MultiPoint::push_p3)
        .def("transform", &MultiPoint::transform)
        .def("serialize", &MultiPoint::serialize)
        .def("deserialize", &MultiPoint::deserialize);


    py::class_<PointCloud, std::shared_ptr<PointCloud>, Model, PyPointCloud>(m, "PointCloud")
        .def(py::init<>())
        .def_property_readonly("type", &PointCloud::type)
        .def("copy", &PointCloud::copy)
        .def("to_obj", &PointCloud::to_obj)
        .def("map", &PointCloud::map)
        .def("slice_to_grid", &PointCloud::slice_to_grid);


    py::class_<MultiLine, std::shared_ptr<MultiLine>, BaseModel, PyMultiLine>(m, "MultiLine")
        .def(py::init<>())
        .def_property_readonly("type", &MultiLine::type)
        .def("push_l2", &MultiLine::push_l2)
        .def("push_l3", &MultiLine::push_l3)
        .def("transform", &MultiLine::transform)
        .def("serialize", &MultiLine::serialize)
        .def("deserialize", &MultiLine::deserialize);


    py::class_<SegmentCloud, std::shared_ptr<SegmentCloud>, Model, PySegmentCloud>(m, "SegmentCloud")
        .def(py::init<>())
        .def_property_readonly("type", &SegmentCloud::type)
        .def("add_attribute", py::overload_cast<const string &, const uint32_t>(&SegmentCloud::add_attribute))
        .def("copy", &SegmentCloud::copy)
        .def("to_obj", &SegmentCloud::to_obj)
        .def("map", &SegmentCloud::map)
        .def("slice_to_grid", &SegmentCloud::slice_to_grid);


    py::class_<MultiPolygon, std::shared_ptr<MultiPolygon>, BaseModel, PyMultiPolygon>(m, "MultiPolygon")
        .def(py::init<>())
        .def_property_readonly("type", &MultiPolygon::type)
        .def("push_p2", &MultiPolygon::push_p2)
        .def("push_p3", &MultiPolygon::push_p3)
        .def("transform", &MultiPolygon::transform)
        .def("serialize", &MultiPolygon::serialize)
        .def("deserialize", &MultiPolygon::deserialize);


    py::class_<TriangularMesh, std::shared_ptr<TriangularMesh>, Model, PyTriangularMesh>(m, "TriangularMesh")
        .def(py::init<>())
        .def_property_readonly("type", &TriangularMesh::type)
        .def("copy", &TriangularMesh::copy)
        .def("to_obj", &TriangularMesh::to_obj)
        .def("map", &TriangularMesh::map)
        .def("slice_to_grid", &TriangularMesh::slice_to_grid);

    py::class_<MultiTimePoint, std::shared_ptr<MultiTimePoint>, BaseModel, PyMultiTimePoint>(m, "MultiTimePoint")
        .def(py::init<>())
        .def_property_readonly("type", &MultiTimePoint::type)
        .def_property_readonly("start_time", &MultiTimePoint::get_start_time)
        .def_property_readonly("end_time", &MultiTimePoint::get_end_time)
        .def_property_readonly("empty", &MultiTimePoint::empty)
        .def("set_points_from_b64", &MultiTimePoint::set_points_from_b64)
        .def("set_start_time", &MultiTimePoint::set_start_time)
        .def("transform", &MultiTimePoint::transform)
        .def("serialize", &MultiTimePoint::serialize)
        .def("deserialize", &MultiTimePoint::deserialize);

    py::class_<LegoBuilder, std::shared_ptr<LegoBuilder>>(m, "LegoBuilder")
        .def(py::init<>())
        .def("insert_model", &LegoBuilder::insert_model)
        .def("build_heightmap", &LegoBuilder::build_heightmap)
        .def("legofy", &LegoBuilder::legofy)
        .def("lego_to_png", &LegoBuilder::lego_to_png);

    py::class_<Interval, std::shared_ptr<Interval>>(m, "Interval")
        .def(py::init<>())
        .def(py::init<uint32_t, uint32_t>())
        .def_property_readonly("start_time", &Interval::get_start_time)
        .def("insert", &Interval::insert)
        .def("can_contain", &Interval::can_contain)
        .def("serialize", &Interval::serialize)
        .def("deserialize", &Interval::deserialize);
}
