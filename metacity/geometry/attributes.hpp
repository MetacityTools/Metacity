#pragma once
#include <vector>
#include "types.hpp"

using namespace std;

struct Attribute
{
    virtual ~Attribute();
    virtual const char * type()const = 0;
    virtual shared_ptr<Attribute> copy() const = 0;
    virtual void join(const shared_ptr<Attribute> a) = 0;
    virtual json serialize() const = 0;
    virtual void deserialize(const string & data) = 0;
};

template <typename T>
struct TAttribute : public Attribute
{
    void join(const shared_ptr<Attribute> a) override
    {
        const shared_ptr<TAttribute<T>> ta = static_pointer_cast<TAttribute<T>>(a);
        data.insert(data.end(), ta->data.begin(), ta->data.end());
    };

    virtual shared_ptr<Attribute> copy() const override;
    virtual const char * type() const override;
    virtual void fill(const T v, const size_t count);
    virtual json serialize() const override;
    virtual void deserialize(const string & data) override;  

    vector<T> data;
};

//===============================================================================
//uint32

template <>
inline  shared_ptr<Attribute> TAttribute<uint32_t>::copy() const
{
    return make_shared<TAttribute<uint32_t>>(TAttribute<uint32_t>(*this));
};

template <>
inline const char * TAttribute<uint32_t>::type() const
{
    return "uint32";
};

template <>
inline void TAttribute<uint32_t>::fill(const uint32_t value, const size_t count)
{
    data.clear();
    data.insert(data.end(), count, value);
};

template <>
inline json TAttribute<uint32_t>::serialize() const 
{
    return { 
        { "type", type() },
        { "data", T_to_string<uint32_t>(data)}
    };
};

template <>
inline void TAttribute<uint32_t>::deserialize(const string & data_)
{
    data = string_to_T<uint32_t>(data_);
};

//===============================================================================
shared_ptr<Attribute> attr_deserialize(const json & attrib);
