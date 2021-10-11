#pragma once
#include <vector>
#include <map>
#include <iostream>
#include "glm/glm.hpp"
#include "json/pybind11_json.hpp"

using namespace std;

using tvec3 = glm::vec3;
using tvec2 = glm::vec2;
using tfloat = float;
using json = nlohmann::json;


class Primitive
{
public:
    virtual ~Primitive();
    //virtual void transform() = 0;
    virtual json serialize() const = 0;
    virtual void deserialize(const json data) = 0;
    vector<float> get_vertices() const;

protected:
    vector<tfloat> vec_to_float(const vector<tvec3> & vec) const;
    vector<uint8_t> vec_to_unit8(const vector<tvec3> & vec) const;
    vector<tvec3> uint8_to_vec(const vector<uint8_t> & bytes) const;
    void append(vector<uint8_t> & vec, tfloat f) const;
    
    vector<tvec3> vertices;
    json tags;
};


class MultiPoint : public Primitive
{
public:
    void push_p2(const vector<tfloat> ivertices);
    void push_p3(const vector<tfloat> ivertices);
    vector<tfloat> contents() const;
    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

protected:
    vector<tvec3> points;
};


class MultiLine : public Primitive
{
public:
    void push_l2(const vector<tfloat> ivertices);
    void push_l3(const vector<tfloat> ivertices);
    vector<vector<tfloat>> contents() const;
    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

protected:
    vector<vector<tvec3>> lines;
};


class MultiPolygon : public Primitive
{
public:
    void push_p2(const vector<vector<tfloat>> ivertices);
    void push_p3(const vector<vector<tfloat>> ivertices);
    vector<vector<vector<tfloat>>> contents() const;
    virtual json serialize() const override;
    virtual void deserialize(const json data) override;
    void triangulate();

protected:
    vector<vector<vector<tvec3>>> polygons;
};


