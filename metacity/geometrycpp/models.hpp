#pragma once
#include <vector>
#include <unordered_map>
#include "types.hpp"
#include "attribute.hpp"

using namespace std;


class Model
{
public:
    Model();
    void add_attribute(const string &name, shared_ptr<Attribute> attribute);
    shared_ptr<Attribute> get_attribute(const string &name);

    

protected:
    unordered_map<string, shared_ptr<Attribute>> attrib;
};

