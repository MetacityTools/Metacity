#include "interval.hpp"


Interval::Interval(): 
start_time(0), end_time(0), length(0) {}

Interval::Interval(uint32_t interval_start_time, uint32_t interval_length) 
: start_time(interval_start_time), end_time(interval_start_time + interval_length), length(interval_length) 
{
    from = vector<vector<tvec3>>(length);    
    to = vector<vector<tvec3>>(length);    
    oid = vector<vector<int32_t>>(length);    
}


uint32_t Interval::insert(shared_ptr<MultiTimePoint> timepoints, int32_t oid_){
    if(!can_contain(timepoints))
        return 0;

    uint32_t trip_start_time = timepoints->get_start_time();
    uint32_t trip_end_time = timepoints->get_end_time() - 1;
    
    uint32_t t_min = max(start_time, trip_start_time);
    uint32_t t_max = min(end_time, trip_end_time);

    uint32_t trip_idx, interval_idx;
    size_t movements = 0;
    for(uint32_t t = t_min; t < t_max; ++t){
        trip_idx = t - trip_start_time;
        interval_idx = t - start_time;
        from[interval_idx].emplace_back(timepoints->points[trip_idx]);
        to[interval_idx].emplace_back(timepoints->points[trip_idx + 1]);
        oid[interval_idx].emplace_back(oid_);
        movements++;
    }
    return movements;
}


bool Interval::can_contain(shared_ptr<MultiTimePoint> timepoints) const{
    uint32_t trip_start_time = timepoints->get_start_time();
    uint32_t trip_end_time = timepoints->get_end_time();

    if( (start_time >= trip_end_time) || (end_time <= trip_start_time))
        return false;
    return true;
}

uint32_t Interval::get_start_time() const{
    return start_time;
}


json Interval::serialize() const
{
    vector<string> vsfrom;
    vector<string> vsto;
    vector<string> vsoid;

    for (size_t i = 0; i < length; ++i)
    {
        vsfrom.emplace_back(vec_to_string(from[i]));
        vsto.emplace_back(vec_to_string(to[i]));
        vsoid.emplace_back(T_to_string<int32_t>(oid[i]));
    }

    return {
        {"start_time", start_time},
        {"length", length},
        {"end_time", end_time},
        {"from", vsfrom},
        {"to", vsto},
        {"oid", vsoid}
    };
}

void Interval::deserialize(const json data)
{
    start_time = data.at("start_time").get<uint32_t>();
    end_time = data.at("start_time").get<uint32_t>();
    length = data.at("length").get<uint32_t>();

    const auto vsfrom = data.at("from").get<vector<string>>();
    const auto vsto = data.at("to").get<vector<string>>();
    const auto vsoid = data.at("oid").get<vector<string>>();

    from.clear();
    to.clear();
    oid.clear();

    for (size_t i = 0; i < length; ++i)
    {
        from.emplace_back(string_to_vec(vsfrom[i]));
        to.emplace_back(string_to_vec(vsto[i]));
        oid.emplace_back(string_to_T<int32_t>(vsoid[i]));
    }
}

