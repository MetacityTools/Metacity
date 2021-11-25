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