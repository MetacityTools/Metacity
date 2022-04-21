#pragma once
#include "models.hpp"

class Segments : public Model
{
public:
    Segments();
    Segments(const vector<tvec3> & v);
    Segments(const vector<tvec3> && v);

    virtual shared_ptr<Model> copy() const override;
    virtual const char * type() const override;
    virtual void add_attribute(const string & name, const uint32_t value) override;
    virtual size_t to_obj(const string & path, const size_t offset) const override;
};