#include <stdexcept>
#include <iostream>
#include "attributes.hpp"
#include "types.hpp"


Attribute::~Attribute() {}

//===============================================================================
shared_ptr<Attribute> attr_deserialize(const json & attrib)
{
    const string type = attrib.at("type").get<string>();
    const string data = attrib.at("data").get<string>();
    shared_ptr<Attribute> attr;

    //this is a bit awful
    if (type == TAttribute<uint32_t>().type())
    {
        attr = make_shared<TAttribute<uint32_t>>();
        attr->deserialize(data);
    } else {
        throw runtime_error("Unsupported attribute type: " + type);
    }

    return attr;
}

