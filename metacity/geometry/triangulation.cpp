#include "triangulation.hpp"

namespace mapbox
{
    namespace util
    {

        template <>
        struct nth<0, K::Point_2>
        {
            inline static auto get(const K::Point_2 &t)
            {
                return t.x();
            };
        };
        template <>
        struct nth<1, K::Point_2>
        {
            inline static auto get(const K::Point_2 &t)
            {
                return t.y();
            };
        };

    } // namespace util
} // namespace mapbox

void Triangulator::triangulate(const Polygons &in_polygons, vector<tvec3> &out_vertices)
{
    mesh.clear();
    tmp_faces.clear();
    to_cgal_mesh(in_polygons);

    for(size_t i = 0; i < tmp_faces.size(); ++i) {
        projected.clear();
        vertexrefs.clear();

        compute_normal(tmp_faces[i]);
        if (normal == CGAL::NULL_VECTOR)
            continue;

        project_pair(in_polygons[i], out_vertices);
        std::vector<uint32_t> indices = mapbox::earcut<uint32_t>(projected);
        for (const auto &i : indices)
            out_vertices.emplace_back(vertexrefs[i]);
    }
}

void Triangulator::to_cgal_mesh(const Polygons &polygons)
{
    tmp_faces.clear();
    Mesh::Face_index fi;
    for (const auto &polygon : polygons)
    {
        tmp_points.clear();
        for (const auto &p : polygon[0])
            tmp_points.push_back(mesh.add_vertex(K::Point_3(p.x, p.y, p.z)));
        fi = mesh.add_face(tmp_points);
        if (fi != Mesh::null_face())
            tmp_faces.push_back(fi);
    }
}

void Triangulator::compute_normal(const Mesh::Face_index fi)
{    
    normal = CGAL::Polygon_mesh_processing::compute_face_normal(fi, mesh);
}

void Triangulator::project_pair(const Polygon &polygon, vector<tvec3> &out_vertices)
{
    const tvec3 &p = polygon[0][0];
    const K::Point_3 point = K::Point_3(p.x, p.y, p.z);
    CGAL::Plane_3<K> plane(point, normal);

    for (const auto &ring : polygon)
    {
        vector<K::Point_2> projected_ring;
        for (const auto &p : ring)
        {
            projected_ring.push_back(plane.to_2d(K::Point_3(p.x, p.y, p.z)));
            vertexrefs.emplace_back(p);
        }
        projected.emplace_back(move(projected_ring));
    }
}