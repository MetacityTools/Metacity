#include "interval.hpp"


Interval::Interval(uint32_t interval_start_time, uint32_t interval_length): start_time(interval_start_time), length(interval_length){}


void Interval::insert(shared_ptr<MultiTimePoint> timepoints, int32_t oid){
    if(!this->can_contain(timepoints)){
        return;
    }

    

}


bool Interval::can_contain(shared_ptr<MultiTimePoint> timepoints){
    uint32_t endtime = timepoints->get_start_time() + timepoints->size();
    if(endtime < start_time)
        return false;
    return true;
}
