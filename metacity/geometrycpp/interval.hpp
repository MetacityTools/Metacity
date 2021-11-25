#pragma once
#include <vector>
#include "types.hpp"
#include "timepoints.hpp"

using namespace std;


class Interval {
public:
    Interval();
    Interval(uint32_t interval_start_time, uint32_t interval_length);
    uint32_t insert(shared_ptr<MultiTimePoint> timepoints, int32_t oid);
    bool can_contain(shared_ptr<MultiTimePoint> timepoints) const;

    uint32_t get_start_time() const;
    json serialize() const;
    void deserialize(const json data);

protected:
    uint32_t start_time;
    uint32_t end_time;
    uint32_t length;
    vector<vector<tvec3>> from;
    vector<vector<tvec3>> to;
    vector<vector<int32_t>> oid;
};