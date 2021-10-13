#pragma once
#include <vector>
#include <unordered_map>
#include <iostream>
#include "types.hpp"

using namespace std;

using tvec3 = glm::vec3;
using tvec2 = glm::vec2;
using tfloat = float;
using json = nlohmann::json;


struct pair_hash {
    size_t operator () (const pair<int,int> &p) const;
};


class Primitive
{
public:
    virtual ~Primitive();
    
    void push_vert(const tvec3 &vec);
    void push_vert(const tvec3 &vec1, const tvec3 &vec2);
    void push_vert(const tvec3 &vec1, const tvec3 &vec2, const tvec3 &vec3);

    virtual json serialize() const;
    virtual void deserialize(const json data);

    virtual const char * type() const = 0;
    virtual void transform() = 0;
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const = 0;

protected:
    vector<tfloat> vec_to_float(const vector<tvec3> & vec) const;
    vector<uint8_t> vec_to_unit8(const vector<tvec3> & vec) const;
    vector<tvec3> uint8_to_vec(const vector<uint8_t> & bytes) const;
    string vec_to_string(const vector<tvec3> & vec) const;
    vector<tvec3> string_to_vec(const string & s) const;
    void append(vector<uint8_t> & vec, tfloat f) const;
    void grid_coords(const tvec3 & point, const float tile_size, pair<int, int> & coords) const;
    
    vector<tvec3> vertices;
    json tags;
};


class MultiPoint : public Primitive
{
public:
    virtual const char * type() const override;
    void push_p2(const vector<tfloat> ivertices);
    void push_p3(const vector<tfloat> ivertices);
    virtual void transform() override;
    vector<tfloat> contents() const;
    virtual json serialize() const override;
    virtual void deserialize(const json data) override;
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override;

protected:
    vector<tvec3> points;
};

using Tiles = unordered_map<pair<int, int>, shared_ptr<Primitive>, pair_hash>;

class SimpleMultiPoint : public Primitive
{
public:
    SimpleMultiPoint();
    SimpleMultiPoint(const MultiPoint & points);
    virtual void transform() override;
    virtual const char * type() const override;
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override;
};


class MultiLine : public Primitive
{
public:
    virtual const char * type() const override;
    void push_l2(const vector<tfloat> ivertices);
    void push_l3(const vector<tfloat> ivertices);
    virtual void transform() override;
    vector<vector<tfloat>> contents() const;
    virtual json serialize() const override;
    virtual void deserialize(const json data) override;
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override;

protected:
    vector<vector<tvec3>> lines;
};

class SimpleMultiLine : public Primitive
{
public:
    SimpleMultiLine();
    SimpleMultiLine(const MultiLine & lines);
    virtual void transform() override;
    virtual const char * type() const override;
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override;

protected:
    void to_tiles(const std::vector<tvec3> &points, const float tile_size, Tiles & tiles) const;
};


class MultiPolygon : public Primitive
{
public:
    virtual const char * type() const override;
    void push_p2(const vector<vector<tfloat>> ivertices);
    void push_p3(const vector<vector<tfloat>> ivertices);
    virtual void transform() override;
    vector<vector<vector<tfloat>>> contents() const;
    virtual json serialize() const override;
    virtual void deserialize(const json data) override;
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override;
    
protected:
    vector<vector<vector<tvec3>>> polygons;
};


class SimpleMultiPolygon : public Primitive
{
public:
    SimpleMultiPolygon(const MultiPolygon & polygons);
    virtual void transform() override;
    virtual const char * type() const override;
    virtual vector<shared_ptr<Primitive>> slice_to_grid(const float tile_size) const override;
};

