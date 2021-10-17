#pragma once
#include "primitives.hpp"

class MultiPolygon : public Primitive
{
public:
    void push_p2(const vector<vector<tfloat>> ivertices);
    void push_p3(const vector<vector<tfloat>> ivertices);

    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

    virtual const char *type() const override;
    virtual shared_ptr<SimplePrimitive> transform() const override;

protected:
    vector<vector<vector<tvec3>>> polygons;
};

class RTree;

class SimpleMultiPolygon : public SimplePrimitive
{
public:
    SimpleMultiPolygon();
    SimpleMultiPolygon(const vector<tvec3> &v);
    SimpleMultiPolygon(const vector<tvec3> &&v);

    virtual shared_ptr<SimplePrimitive> copy() const override;
    virtual const char *type() const override;
    virtual shared_ptr<SimplePrimitive> transform() const override;
    virtual vector<shared_ptr<SimplePrimitive>> slice_to_grid(const float tile_size) const override;
    virtual void map(const shared_ptr<SimpleMultiPolygon> target) override;

    const tvec3 * triangle(const size_t index) const;
    const shared_ptr<Attribute> attribute(const string & name);

protected:
    void to_tiles(const vector<tvec3> &triangles, const float tile_size, Tiles &tiles) const;
    friend class RTree;
};
