#pragma once
#include "models.hpp"


class Points : public Model
{
public:
    Points();
    Points(const vector<tvec3> & v);
    Points(const vector<tvec3> && v);

    virtual shared_ptr<Model> copy() const override;
    virtual const char * type() const override;
    virtual size_t to_obj(const string & path, const size_t offset) const override;
};