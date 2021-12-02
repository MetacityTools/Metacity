#include "interval.hpp"


Interval::Interval(): 
start_time(0), end_time(0), length(0) {}

Interval::Interval(uint32_t interval_start_time, uint32_t interval_length) 
: start_time(interval_start_time), end_time(interval_start_time + interval_length), length(interval_length) 
{
    from = vector<vector<tvec3>>(length);    
    to = vector<vector<tvec3>>(length);    
    oid = vector<vector<int32_t>>(length);    
    from_speed = vector<vector<tfloat>>(length);    
    to_speed = vector<vector<tfloat>>(length);    
}


uint32_t Interval::insert(shared_ptr<MultiTimePoint> timepoints, int32_t oid_){
    if(!can_contain(timepoints))
        return 0;

    uint32_t trip_start_time = timepoints->get_start_time();
    uint32_t trip_end_time = timepoints->get_end_time() - 2; 
    
    uint32_t t_min = max(start_time, trip_start_time);
    uint32_t t_max = min(end_time, trip_end_time);

    uint32_t trip_idx, interval_idx;
    size_t movements = 0;
    for(uint32_t t = t_min; t < t_max; ++t){
        trip_idx = t - trip_start_time;
        interval_idx = t - start_time;
        from_speed[interval_idx].emplace_back(glm::length(timepoints->points[trip_idx] - timepoints->points[trip_idx + 1]));
        to_speed[interval_idx].emplace_back(glm::length(timepoints->points[trip_idx + 1] - timepoints->points[trip_idx + 2]));
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
    vector<string> vsfrom_speed;
    vector<string> vsto;
    vector<string> vsto_speed;
    vector<string> vsoid;

    for (size_t i = 0; i < length; ++i)
    {
        vsfrom.emplace_back(vec_to_string(from[i]));
        vsfrom_speed.emplace_back(T_to_string<tfloat>(from_speed[i]));
        vsto.emplace_back(vec_to_string(to[i]));
        vsto_speed.emplace_back(T_to_string<tfloat>(to_speed[i]));
        vsoid.emplace_back(T_to_string<int32_t>(oid[i]));
    }

    return {
        {"start_time", start_time},
        {"length", length},
        {"end_time", end_time},
        {"from", vsfrom},
        {"from_speed", vsfrom_speed},
        {"to", vsto},
        {"to_speed", vsto_speed},
        {"oid", vsoid}
    };
}

json Interval::serialize_stream() const
{
    vector<string> vsfrom;
    vector<string> vsfrom_speed;
    vector<float>  vffrom_speed;
    vector<string> vsto;
    vector<string> vsto_speed;
    vector<float>  vfto_speed;
    vector<string> vsoid;


    for (size_t i = 0; i < length; ++i)
    {
        vffrom_speed.clear();
        vfto_speed.clear();

        copy(from_speed[i].begin(), from_speed[i].end(), back_inserter(vffrom_speed));
        copy(to_speed[i].begin(), to_speed[i].end(), back_inserter(vfto_speed));

        vsfrom.emplace_back(vec_to_f_to_string(from[i]));
        vsfrom_speed.emplace_back(T_to_string<float>(vffrom_speed));
        vsto.emplace_back(vec_to_f_to_string(to[i]));
        vsto_speed.emplace_back(T_to_string<float>(vfto_speed));
        vsoid.emplace_back(T_to_string<int32_t>(oid[i]));
    }

    return {
        {"start_time", start_time},
        {"length", length},
        {"end_time", end_time},
        {"from", vsfrom},
        {"from_speed", vsfrom_speed},
        {"to", vsto},
        {"to_speed", vsto_speed},
        {"oid", vsoid}
    };  
}

void Interval::deserialize(const json data)
{
    start_time = data.at("start_time").get<uint32_t>();
    end_time = data.at("end_time").get<uint32_t>();
    length = data.at("length").get<uint32_t>();

    const auto vsfrom = data.at("from").get<vector<string>>();
    const auto vsfrom_speed = data.at("from_speed").get<vector<string>>();
    const auto vsto = data.at("to").get<vector<string>>();
    const auto vsto_speed = data.at("to_speed").get<vector<string>>();
    const auto vsoid = data.at("oid").get<vector<string>>();

    from.clear();
    to.clear();
    oid.clear();
    from_speed.clear();
    to_speed.clear();

    for (size_t i = 0; i < length; ++i)
    {
        from.emplace_back(string_to_vec(vsfrom[i]));
        to.emplace_back(string_to_vec(vsto[i]));
        oid.emplace_back(string_to_T<int32_t>(vsoid[i]));
        from_speed.emplace_back(string_to_T<tfloat>(vsfrom_speed[i]));
        to_speed.emplace_back(string_to_T<tfloat>(vsto_speed[i]));
    }
}

