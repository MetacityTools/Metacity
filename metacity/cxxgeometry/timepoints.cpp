#include "timepoints.hpp"


void MultiTimePoint::set_points_from_b64(const string & data){
    points = string_to_vec2_to_vec3(data);
}

void MultiTimePoint::set_start_time(const uint32_t & start_time) {
    start = start_time;
}

const uint32_t MultiTimePoint::get_start_time(){
    return(start);
}

const uint32_t MultiTimePoint::size(){
    return(points.size());
}

const char * MultiTimePoint::type() const {
    return "timepoint";
}

json MultiTimePoint::serialize() const
{
    json data = Primitive::serialize();
    data["points"] = vec_to_string(points);
    data["start"] = start;
    return data;
}

void MultiTimePoint::deserialize(const json data)
{
    const auto spoints = data.at("points").get<string>();
    points = string_to_vec(spoints);

    start = data.at("start").get<uint32_t>();
    Primitive::deserialize(data);
};


shared_ptr<SimplePrimitive> MultiTimePoint::transform() const
{
    return nullptr;
};