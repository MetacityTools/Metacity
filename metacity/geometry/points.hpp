#pragma once
#include "primitives.hpp"


class MultiPoint : public Primitive
{
public:
    void push_p2(const vector<tfloat> ivertices);
    void push_p3(const vector<tfloat> ivertices);

    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

    virtual const char * type() const override;
    virtual shared_ptr<SimplePrimitive> transform() const override;
protected:

    vector<tvec3> points;
};

class SimpleMultiPoint : public SimplePrimitive
{
public:
    SimpleMultiPoint();
    SimpleMultiPoint(const vector<tvec3> & v);
    SimpleMultiPoint(const vector<tvec3> && v);

    virtual shared_ptr<SimplePrimitive> copy() const override;
    virtual const char * type() const override;
    virtual vector<shared_ptr<SimplePrimitive>> slice_to_grid(const tfloat tile_size) const override;
    virtual void map(const shared_ptr<SimpleMultiPolygon> target) override;

    virtual size_t to_obj(const string & path, const size_t offset) const override;
};