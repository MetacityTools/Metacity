#include "triangulation.hpp"

namespace mapbox
{
    namespace util
    {

        template <>
        struct nth<0, K::Point_2>
        {
            inline static tfloat get(const K::Point_2 &t)
            {
                return t.x();
            };
        };
        template <>
        struct nth<1, K::Point_2>
        {
            inline static tfloat get(const K::Point_2 &t)
            {
                return t.y();
            };
        };

    } // namespace util
} // namespace mapbox

void Triangulator::triangulate(const Polygons &in_polygons, vector<tvec3> &out_vertices)
{
    if (in_polygons.size() == 0)
        return;
    
    mesh.clear();
    tmp_faces.clear();

    for(const auto & polygon : in_polygons) {
        if (!to_cgal_mesh(polygon))
            continue;

        projected.clear();
        vertexrefs.clear();

        compute_normal(tmp_faces.back());
        if (normal == CGAL::NULL_VECTOR)
            continue;

        project_pair(polygon);
        std::vector<uint32_t> indices = mapbox::earcut<uint32_t>(projected);
        for (const auto &i : indices)
            out_vertices.emplace_back(vertexrefs[i]);
    }
}

void Triangulator::triangulate(const SimplePolygon &in_polygon, vector<tvec3> &out_vertices)
{
    mesh.clear();
    tmp_faces.clear();
    projected.clear();
    vertexrefs.clear();

    if(!to_cgal_mesh(in_polygon))
        return;

    compute_normal(tmp_faces[0]);
    if (normal == CGAL::NULL_VECTOR)
        return;

    project_pair(in_polygon);
    std::vector<uint32_t> indices = mapbox::earcut<uint32_t>(projected);
    for (const auto &i : indices)
        out_vertices.emplace_back(vertexrefs[i]);
}

bool Triangulator::to_cgal_mesh(const Polygon &polygon)
{
    tmp_faces.clear();
    Mesh::Face_index fi;
    tmp_points.clear();

    if (polygon.size() == 0)
        return false;

    if (polygon[0].size() < 3)
        return false;

    for (const auto &p : polygon[0])
        tmp_points.push_back(mesh.add_vertex(K::Point_3(p.x, p.y, p.z)));
    
    fi = mesh.add_face(tmp_points);
    if (fi != Mesh::null_face())
        tmp_faces.push_back(fi);

    return true;
}

bool Triangulator::to_cgal_mesh(const SimplePolygon &polygon)
{
    tmp_faces.clear();
    tmp_points.clear();
    Mesh::Face_index fi;

    if (polygon.size() < 3)
        return false;

    for (const auto &p : polygon)
        tmp_points.push_back(mesh.add_vertex(p));
    fi = mesh.add_face(tmp_points);
    if (fi != Mesh::null_face())
        tmp_faces.push_back(fi);

    return true;
}

void Triangulator::compute_normal(const Mesh::Face_index fi)
{    
    normal = CGAL::Polygon_mesh_processing::compute_face_normal(fi, mesh);
}

void Triangulator::project_pair(const Polygon &polygon)
{
    const tvec3 &p = polygon[0][0];
    const K::Point_3 point = K::Point_3(p.x, p.y, p.z);
    CGAL::Plane_3<K> plane(point, normal);

    for (const auto &ring : polygon)
    {
        vector<K::Point_2> projected_ring;
        for (const auto &p : ring)
        {
            projected_ring.push_back(plane.to_2d(K::Point_3(p.x, p.y, p.z))); //to_2D behaves sus
            vertexrefs.emplace_back(p);
        }
        projected.emplace_back(move(projected_ring));
    }
}

void Triangulator::project_pair(const SimplePolygon &polygon)
{
    const K::Point_3 &point = polygon[0];
    CGAL::Plane_3<K> plane(point, normal);
    vector<K::Point_2> projected_ring;
    for (const auto &p : polygon)
    {
        projected_ring.push_back(plane.to_2d(p));
        vertexrefs.emplace_back(to_vec(p));
    }
    projected.emplace_back(move(projected_ring));
}