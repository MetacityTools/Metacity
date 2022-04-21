#pragma once
#include "models.hpp"


class MultiPoint : public ModelLoader
{
public:
    void push_p2(const vector<tfloat> ivertices);
    void push_p3(const vector<tfloat> ivertices);

    virtual const char * type() const override;
    virtual shared_ptr<Model> transform() const override;
protected:

    vector<tvec3> points;
};

class MultiLine : public ModelLoader
{
public:
    void push_l2(const vector<tfloat> ivertices);
    void push_l3(const vector<tfloat> ivertices);

    virtual const char * type() const override;
    virtual shared_ptr<Model> transform() const override;
protected:
    vector<vector<tvec3>> lines;
};


class MultiPolygon : public ModelLoader
{
public:
    void push_p2(const vector<vector<tfloat>> ivertices);
    void push_p3(const vector<vector<tfloat>> ivertices);

    virtual const char *type() const override;
    virtual shared_ptr<Model> transform() const override;

protected:
    vector<vector<vector<tvec3>>> polygons;
};
