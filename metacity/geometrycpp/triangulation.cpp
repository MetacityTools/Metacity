#include "triangulation.hpp"

namespace mapbox
{
    namespace util
    {

        template <>
        struct nth<0, tvec2>
        {
            inline static tfloat get(const tvec2 &t)
            {
                return t.x;
            };
        };
        template <>
        struct nth<1, tvec2>
        {
            inline static tfloat get(const tvec2 &t)
            {
                return t.y;
            };
        };

    } // namespace util
} // namespace mapbox


void Triangulator::to_output(const vector<vector<tvec3>> & polygon, vector<uint32_t> & indices, vector<tvec3> &out_vertices) const
{
     for (auto &i : indices)
    {
        for (const auto &ring : polygon)
        {
            if (i < ring.size())
            {
                out_vertices.push_back(ring[i]);
                break;
            }
            i -= ring.size();
        }
    }
}

void Triangulator::triangulate(const vector<vector<vector<tvec3>>> &in_polygon, vector<tvec3> &out_vertices)
{
    if (in_polygon.size() == 0)
        return;
    
    out_vertices.clear();

    for (const auto & polygon : in_polygon)
    {
        projected.clear();
        
        tvec3 normal = compute_polygon_with_holes_normal(polygon);
        project_along_normal(polygon, normal);
        vector<uint32_t> indices = mapbox::earcut<uint32_t>(projected);
        to_output(polygon, indices, out_vertices);
    }
}

tvec3 Triangulator::compute_polygon_with_holes_normal(const vector<vector<tvec3>> & in_polygon) const
{
    tvec3 normal;
    for (const auto & polygon : in_polygon)
    {
        tvec3 polygon_normal = tvec3(0, 0, 0);
        for (size_t i = 0; i < polygon.size(); i++)
        {
            tvec3 v1 = polygon[i];
            tvec3 v2 = polygon[(i + 1) % polygon.size()];
            polygon_normal += cross(v1, v2);
        }
        normal += polygon_normal;
    }
    normal = normalize(normal);
    return normal;
}

void Triangulator::project_along_normal(const vector<vector<tvec3>> & in_polygon, const tvec3 & normal)
{
    for (const auto & polygon : in_polygon)
    {
        vector<tvec2> projected_polygon;
        for (const auto & v : polygon)
        {
            tvec3 projected_vertex = v - dot(v, normal) * normal;
            projected_polygon.emplace_back(projected_vertex);
        }
        projected.emplace_back(move(projected_polygon));
    }
}