#pragma once
#include "models.hpp"


class Interval;
class MultiTimePoint;
class RTree;

class MultiTimePointMapper {
public: 
    MultiTimePointMapper(const vector<shared_ptr<TriangularMesh>> target);
protected:
    shared_ptr<RTree> tree;
    friend class MultiTimePoint;
};


class MultiTimePoint : public BaseModel {
public: 
    void set_points_from_b64(const string & data);
    void set_start_time(const uint32_t & start_time);

    const uint32_t get_start_time() const;
    const uint32_t get_end_time() const;
    const bool empty() const;
    vector<shared_ptr<MultiTimePoint>> slice_to_timeline(const uint32_t interval_size) const;

    virtual json serialize() const override;
    virtual void deserialize(const json data) override;

    virtual const char * type() const override;
    virtual shared_ptr<Model> transform() const override;
    shared_ptr<MultiTimePoint> copy() const;
    
    void map(const shared_ptr<MultiTimePointMapper> mapper);
    
protected:
    uint32_t start;
    vector<tvec3> points;

    friend class Interval;
};



