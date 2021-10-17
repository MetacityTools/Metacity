#pragma once
#include "primitives.hpp"


class MultiLine : public Primitive
{
public:
    void push_l2(const vector<tfloat> ivertices);
    void push_l3(const vector<tfloat> ivertices);

    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

    virtual const char * type() const override;
    virtual shared_ptr<SimplePrimitive> transform() const override;
protected:
    vector<vector<tvec3>> lines;
};

class SimpleMultiLine : public SimplePrimitive
{
public:
    SimpleMultiLine();
    SimpleMultiLine(const vector<tvec3> & v);
    SimpleMultiLine(const vector<tvec3> && v);

    virtual shared_ptr<SimplePrimitive> copy() const override;
    virtual const char * type() const override;
    virtual shared_ptr<SimplePrimitive> transform() const override;
    virtual vector<shared_ptr<SimplePrimitive>> slice_to_grid(const float tile_size) const override;
    virtual void map(const shared_ptr<SimpleMultiPolygon> target) override;

protected:
    void to_tiles(const std::vector<tvec3> &points, const float tile_size, Tiles & tiles) const;
};