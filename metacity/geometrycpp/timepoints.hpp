#pragma once
#include "models.hpp"

class Interval;

class MultiTimePoint : public BaseModel {
public: 
    void set_points_from_b64(const string & data);
    void set_start_time(const uint32_t & start_time);

    const uint32_t get_start_time() const;
    const uint32_t get_end_time() const;
    const bool empty() const;

    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

    virtual const char * type() const override;
    virtual shared_ptr<Model> transform() const override;
    
protected:
    uint32_t start;
    vector<tvec3> points;

    friend class Interval;
};



