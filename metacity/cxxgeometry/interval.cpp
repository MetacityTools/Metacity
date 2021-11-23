#include "interval.hpp"


Interval::Interval(uint32_t interval_start_time, uint32_t interval_length): start_time(interval_start_time), length(interval_length){}


void Interval::insert(shared_ptr<MultiTimePoint> timepoints, int32_t oid){
    if(!this->can_contain(timepoints)){
        return;
    }

    uint32_t trip_start_time = timepoints->get_start_time();
    uint32_t trip_end_time = timepoints->get_end_time();
    uint32_t interval_end_time = start_time + length;
    
    uint32_t t_min = max(start_time, trip_start_time);
    uint32_t t_max = min(interval_end_time, trip_end_time);

    if(t_max < t_min)
        return;

    for(uint32_t t = t_min; t < t_max; ++t){
        uint32_t trip_idx = t - trip_start_time;
        tvec3 from = (*timepoints)[trip_idx];
        tvec3 to = (*timepoints)[trip_idx+1];
        buffers[t % length].emplace_back(Movement(from, to, oid));
    }
}


bool Interval::can_contain(shared_ptr<MultiTimePoint> timepoints) const{
    uint32_t trip_end_time = timepoints->get_end_time();
    uint32_t trip_start_time = timepoints->get_start_time();
    uint32_t end_time = start_time + length;

    if( (start_time >= trip_end_time) || (end_time <= trip_start_time))
        return false;
    return true;
}

