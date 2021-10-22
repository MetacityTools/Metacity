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

class SimpleMultiPolygon;

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
    tuple<tuple<tfloat, tfloat, tfloat>, tuple<tfloat, tfloat, tfloat>> bounding_box() const;
    tvec3 centroidvec() const;
    
    void shift(const tfloat sx, const tfloat sy, const tfloat sz);

    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

    virtual void add_attribute(const string & name, const uint32_t value);
    virtual void add_attribute(const string & name, const shared_ptr<Attribute> attr);

    virtual shared_ptr<SimplePrimitive> copy() const = 0;
    virtual const char * type() const override = 0;
    virtual shared_ptr<SimplePrimitive> transform() const override;
    virtual vector<shared_ptr<SimplePrimitive>> slice_to_grid(const tfloat tile_size) const = 0;

    virtual void map(const shared_ptr<SimpleMultiPolygon> target) = 0;
    bool mapping_ready() const;

    virtual size_t to_obj(const string & path, const size_t offset) const = 0;

protected:
    void copy_to(shared_ptr<SimplePrimitive> cp) const;
    void init_proxy(const shared_ptr<TAttribute<uint32_t>> soid, const shared_ptr<TAttribute<uint32_t>> toid, const vector<tvec3> & nv);

    vector<tvec3> vertices;
    unordered_map<string, shared_ptr<Attribute>> attrib;
};

using Tiles = unordered_map<pair<int, int>, shared_ptr<SimplePrimitive>, pair_hash>;

