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

void Triangulator::triangulate(const Polygon &in_polygon, vector<tvec3> &out_vertices)
{
    clear();
    to_cgal_mesh(in_polygon);
    compute_normal();
    if (normal == CGAL::NULL_VECTOR)
        return;

    project_pair(in_polygon, out_vertices);
    std::vector<uint32_t> indices = mapbox::earcut<uint32_t>(projected);
    for (const auto &i : indices)
    {
        out_vertices.emplace_back(vertexrefs[i]);
    }
}

void Triangulator::clear()
{
    mesh.clear();
    tmp_points.clear();
    projected.clear();
    vertexrefs.clear();
}

void Triangulator::to_cgal_mesh(const Polygon &polygon)
{
    for (const auto &p : polygon[0])
        tmp_points.push_back(mesh.add_vertex(K::Point_3(p.x, p.y, p.z)));
    mesh.add_face(tmp_points);
}

void Triangulator::compute_normal()
{
    Mesh::Property_map fnormals = mesh.add_property_map<Mesh::face_index, K::Vector_3>("f:normals", CGAL::NULL_VECTOR).first;
    CGAL::Polygon_mesh_processing::compute_face_normals(mesh, fnormals);

    if (mesh.num_faces() > 1)
    {
        //this can be done better...
        normal = CGAL::NULL_VECTOR;
    }
    else
    {
        const auto face_index = mesh.faces_begin();
        normal = fnormals[*face_index];
    }
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