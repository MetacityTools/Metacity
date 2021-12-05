#pragma once
#include "models.hpp"

class MultiPolygon : public BaseModel
{
public:
    void push_p2(const vector<vector<tfloat>> ivertices);
    void push_p3(const vector<vector<tfloat>> ivertices);

    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

    virtual const char *type() const override;
    virtual shared_ptr<Model> transform() const override;

protected:
    vector<vector<vector<tvec3>>> polygons;
};

class RTree;
class LegoBuilder;

class TriangularMesh : public Model
{
public:
    TriangularMesh();
    TriangularMesh(const vector<tvec3> &v);
    TriangularMesh(const vector<tvec3> &&v);

    virtual shared_ptr<Model> copy() const override;
    virtual const char *type() const override;
    virtual vector<shared_ptr<Model>> slice_to_grid(const tfloat tile_size) const override;
    shared_ptr<Model> slice_to_rect(const tfloat lower_x, const tfloat lower_y, const tfloat upper_x, const tfloat upper_y) const;
    virtual void map(const shared_ptr<TriangularMesh> target2D) override;

    const tvec3 * triangle(const size_t index) const;
    const shared_ptr<Attribute> attribute(const string & name);

    virtual size_t to_obj(const string & path, const size_t offset) const override;
protected:
    void to_model(const vector<tvec3> &triangles, shared_ptr<TriangularMesh> model) const;
    void to_tiles(const vector<tvec3> &triangles, const tfloat tile_size, Tiles &tiles) const;
    
    friend class RTree;
    friend class LegoBuilder;
};
