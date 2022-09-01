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


tvec2 project_3d_to_2d(const tvec3 & v, const tvec3 & xnormal, const tvec3 & ynormal)
{
    return tvec2(
        glm::dot(v, xnormal),
        glm::dot(v, ynormal)
    );
}

void init_newell_normals_projection(const tvec3 & normal, tvec3 & xnormal, tvec3 & ynormal)
{
    xnormal = tvec3(1.1, 1.1, 1.1);
    if (xnormal == normal)
        xnormal += tvec3(1, 2, 3);
    xnormal = xnormal - glm::dot(xnormal, normal) * normal;
    xnormal = glm::normalize(xnormal);
    ynormal = glm::cross(normal, xnormal);
}

void project_along_normal(const vector<vector<tvec3>> & polygon, const tvec3 & normal, vector<vector<tvec2>> & projected_polygon)
{
    tvec3 x3, y3;
    init_newell_normals_projection(normal, x3, y3);
    for (const auto & ring : polygon)
    {
        vector<tvec2> projected_ring;
        for (const auto & v : ring)
        {
            tvec2 projected_vertex = project_3d_to_2d(v, x3, y3);
            projected_ring.emplace_back(projected_vertex);
        }
        projected_polygon.emplace_back(move(projected_ring));
    }
}

tvec3 compute_polygon_with_holes_normal(const vector<vector<tvec3>> & polygon)
{
    tvec3 normal(0, 0, 0);
    for (const auto & ring : polygon)
    {
        tvec3 polygon_normal(0, 0, 0);
        for (size_t i = 0; i < ring.size(); i++)
        {
            tvec3 v1 = ring[i];
            tvec3 v2 = ring[(i + 1) % ring.size()];
            tvec3 v3 = ring[(i + 2) % ring.size()];
            polygon_normal += cross(v2 - v1, v3 - v2);
        }
        normal += polygon_normal;
    }
    
    if (glm::length(normal) == 0)
    {
        //throw std::runtime_error("Polygon is degenerate");
        return tvec3(0, 0, 0);
    }

    normal = glm::normalize(normal);
    return normal;
}

void to_output(const vector<vector<tvec3>> & polygon, vector<uint32_t> & indices, vector<tvec3> &out_vertices)
{
    for (auto i : indices) {
        for (const auto & ring : polygon) {
            if (ring.size() > i) {
                out_vertices.push_back(ring[i]);
                break;
            }
            i -= ring.size();
        }
    }
}

void triangulate(const vector<vector<tvec3>> & polygon, vector<tvec3> &out_vertices)
{
    if (polygon.size() == 0)
        return;
    
    tvec3 normal = compute_polygon_with_holes_normal(polygon);
    vector<vector<tvec2>> projected_polygon;
    project_along_normal(polygon, normal, projected_polygon);
    vector<uint32_t> indices = mapbox::earcut<uint32_t>(projected_polygon);
    to_output(polygon, indices, out_vertices);
}