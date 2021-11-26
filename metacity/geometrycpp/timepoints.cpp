#include "timepoints.hpp"


void MultiTimePoint::set_points_from_b64(const string & data){
    points = string_to_vec2_to_vec3(data);
}

void MultiTimePoint::set_start_time(const uint32_t & start_time) {
    start = start_time;
}

const uint32_t MultiTimePoint::get_start_time() const {
    return(start);
}

const uint32_t MultiTimePoint::get_end_time() const {
    return get_start_time() + points.size();
}

const bool MultiTimePoint::empty() const{
    return points.size() == 0;
}

const char * MultiTimePoint::type() const {
    return "timepoint";
}

vector<shared_ptr<MultiTimePoint>> MultiTimePoint::slice_to_timeline(const uint32_t interval_size) const
{
    vector<shared_ptr<MultiTimePoint>> submodels;
    uint32_t start_trip_time = start;
    uint32_t start_interval_time = (start_trip_time / interval_size) * interval_size;
    uint32_t end_trip_time = get_end_time();
    uint32_t end_interval_time = ((end_trip_time - 1) / interval_size) * interval_size;

    for (; start_interval_time <= end_interval_time; start_interval_time += interval_size)
    {
        uint32_t segment_start = max(start_trip_time, start_interval_time) - start_trip_time;
        uint32_t segment_end = min(end_trip_time, start_interval_time + interval_size) - start_trip_time;

        auto segment = make_shared<MultiTimePoint>();
        segment->set_start_time(segment_start + start_trip_time);
        segment->points.insert(segment->points.end(), points.begin() + segment_start, points.begin() + segment_end);
        submodels.push_back(segment);
    }    

    return submodels;
}

json MultiTimePoint::serialize() const
{
    json data = BaseModel::serialize();
    data["points"] = vec_to_string(points);
    data["start"] = start;
    return data;
}

void MultiTimePoint::deserialize(const json data)
{
    const auto spoints = data.at("points").get<string>();
    points = string_to_vec(spoints);

    start = data.at("start").get<uint32_t>();
    BaseModel::deserialize(data);
}


shared_ptr<Model> MultiTimePoint::transform() const
{
    return nullptr;
}