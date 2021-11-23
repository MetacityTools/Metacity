#include "interval.hpp"


Interval::Interval(uint32_t interval_start_time, uint32_t interval_length): start_time(interval_start_time), length(interval_length){}


void Interval::insert(shared_ptr<MultiTimePoint> timepoints, int32_t oid){
    if(!this->can_contain(timepoints)){
        return;
    }

    uint32_t trip_start_time = timepoints->get_start_time();
    uint32_t trip_end_time = timepoints->get_end_time();
    uint32_t t_min = max(start_time, trip_start_time);
    uint32_t t_max = min(start_time + length, trip_end_time);

    if(t_max < t_min)
        return;

    for(uint32_t t = t_min; t < t_max; ++t){
        tvec3 from = (*timepoints)[t];
        tvec3 to = (*timepoints)[t+1];
        buffers[t-t_min].emplace_back(Movement(from, to, oid));
    }
}


bool Interval::can_contain(shared_ptr<MultiTimePoint> timepoints){
    uint32_t trip_end_time = timepoints->get_end_time();
    uint32_t trip_start_time = timepoints->get_start_time();
    uint32_t interval_end_time = start_time + length;

    if( (trip_end_time < start_time) || (interval_end_time < trip_start_time))
        return false;
    return true;
}
