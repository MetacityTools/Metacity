#pragma once
#include "models.hpp"


class MultiLine : public BaseModel
{
public:
    void push_l2(const vector<tfloat> ivertices);
    void push_l3(const vector<tfloat> ivertices);

    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

    virtual const char * type() const override;
    virtual shared_ptr<Model> transform() const override;
protected:
    vector<vector<tvec3>> lines;
};


class SegmentCloud : public Model
{
public:
    SegmentCloud();
    SegmentCloud(const vector<tvec3> & v);
    SegmentCloud(const vector<tvec3> && v);

    virtual shared_ptr<Model> copy() const override;
    virtual const char * type() const override;
    virtual void add_attribute(const string & name, const uint32_t value) override;
    virtual vector<shared_ptr<Model>> slice_to_grid(const tfloat tile_size) const override;
    virtual void map(const shared_ptr<TriangularMesh> target) override;

    virtual size_t to_obj(const string & path, const size_t offset) const override;

protected:
    void to_tiles(const std::vector<tvec3> &points, const tfloat tile_size, Tiles & tiles) const;
};