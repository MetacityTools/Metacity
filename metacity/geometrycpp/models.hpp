#pragma once
#include <vector>
#include <unordered_map>
#include "attributes.hpp"


class Model;

class BaseModel
{
public:
    virtual ~BaseModel();
    void add_tag(const string key, const int32_t value);
    json get_tags() const;
    virtual const char * type() const = 0;
protected:
    json tags;
};


class ModelLoader : public BaseModel
{
public:
    virtual shared_ptr<Model> transform() const = 0;
};


class Model: public BaseModel
{
public:
    Model();
    Model(const vector<tvec3> & v);
    Model(const vector<tvec3> && v);

    tuple<tfloat, tfloat, tfloat> centroid() const;
    tuple<tuple<tfloat, tfloat, tfloat>, tuple<tfloat, tfloat, tfloat>> bounding_box() const;    
    
    void shift(const tfloat sx, const tfloat sy, const tfloat sz);
    
    virtual json serialize() const;
    virtual void deserialize(const json data);

    virtual void add_attribute(const string & name, const uint32_t value);
    virtual void add_attribute(const string & name, const shared_ptr<Attribute> attr);

    virtual shared_ptr<Model> copy() const = 0;
    virtual const char * type() const override = 0;
    virtual size_t to_obj(const string & path, const size_t offset) const = 0;

protected:
    void copy_to(shared_ptr<Model> cp) const;

    vector<tvec3> vertices;
    unordered_map<string, shared_ptr<Attribute>> attrib;
};

