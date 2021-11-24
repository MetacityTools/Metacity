#include "interval.hpp"


Interval::Interval(uint32_t interval_start_time, uint32_t interval_length): start_time(interval_start_time), end_time(interval_start_time + interval_length), length(interval_length){}


void Interval::insert(shared_ptr<MultiTimePoint> timepoints, int32_t oid){
    if(!can_contain(timepoints))
        return;

    uint32_t trip_start_time = timepoints->get_start_time();
    uint32_t trip_end_time = timepoints->get_end_time() - 1;
    
    uint32_t t_min = max(start_time, trip_start_time);
    uint32_t t_max = min(end_time, trip_end_time);

    uint32_t trip_idx, interval_idx;
    for(uint32_t t = t_min; t < t_max; ++t){
        trip_idx = t - trip_start_time;
        interval_idx = t - start_time;
        buffers[interval_idx].emplace_back(
            Movement(timepoints->points[trip_idx], timepoints->points[trip_idx + 1], oid));
    }
}


bool Interval::can_contain(shared_ptr<MultiTimePoint> timepoints) const{
    uint32_t trip_start_time = timepoints->get_start_time();
    uint32_t trip_end_time = timepoints->get_end_time();

    if( (start_time >= trip_end_time) || (end_time <= trip_start_time))
        return false;
    return true;
}

