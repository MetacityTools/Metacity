#pragma once
#include <vector>
#include <unordered_map>
#include "attributes.hpp"


class SimplePrimitive;

class Primitive
{
public:
    virtual ~Primitive();
    virtual json serialize() const;
    virtual void deserialize(const json data);

    virtual const char * type() const = 0;
    virtual shared_ptr<SimplePrimitive> transform() const = 0;
protected:
    json tags;
};


class SimplePrimitive: public Primitive
{
public:
    SimplePrimitive();
    SimplePrimitive(const vector<tvec3> & v);
    SimplePrimitive(const vector<tvec3> && v);

    void join(const shared_ptr<SimplePrimitive> primitive);
    void push_vert(const tvec3 &vec);
    void push_vert(const tvec3 * vec, size_t count);
    tuple<tfloat, tfloat, tfloat> centroid() const;

    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

    virtual void add_attribute(const string & name, const uint32_t value);
    virtual void add_attribute(const string & name, const shared_ptr<Attribute> attr);

    virtual shared_ptr<SimplePrimitive> copy() const = 0;
    virtual const char * type() const override = 0;
    virtual shared_ptr<SimplePrimitive> transform() const override = 0;
    virtual vector<shared_ptr<SimplePrimitive>> slice_to_grid(const float tile_size) const = 0;

protected:
    void copy_to(shared_ptr<SimplePrimitive> cp) const;

    vector<tvec3> vertices;
    unordered_map<string, shared_ptr<Attribute>> attrib;
};

using Tiles = unordered_map<pair<int, int>, shared_ptr<SimplePrimitive>, pair_hash>;

