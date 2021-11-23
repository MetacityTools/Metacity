#pragma once
#include "primitives.hpp"


class MultiTimePoint : public Primitive {
public: 
    void set_points_from_b64(const string & data);
    void set_start_time(const uint32_t & start_time);

    uint32_t const get_start_time();
    uint32_t const size();

    const tvec3 & operator[] (const size_t t) const;

    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

    virtual const char * type() const override;
    virtual shared_ptr<SimplePrimitive> transform() const override;
    
protected:
    uint32_t start;
    vector<tvec3> points;
};

inline const tvec3 & MultiTimePoint::operator[] (const size_t t) const{
    return points[t];
}


