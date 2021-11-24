#pragma once
#include <vector>
#include "types.hpp"
#include "timepoints.hpp"

using namespace std;

struct Movement {
    Movement(const tvec3 & x, const tvec3 & y, const int32_t id): from(x), to(y), oid(id) {}

    tvec3 from;
    tvec3 to;
    int32_t oid;
};

class Interval {
public:
    Interval(uint32_t interval_start_time, uint32_t interval_length);
    void insert(shared_ptr<MultiTimePoint> timepoints, int32_t oid);
    bool can_contain(shared_ptr<MultiTimePoint> timepoints) const;

protected:
    uint32_t start_time;
    uint32_t end_time;
    uint32_t length;
    vector<vector<Movement>> buffers;
};