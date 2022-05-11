#include <stdexcept>
#include <fstream>
#include "mesh.hpp"
#include "triangulation.hpp"

//===============================================================================

Mesh::Mesh() : Model() {}
Mesh::Mesh(const vector<tvec3> &v) : Model(v) {}
Mesh::Mesh(const vector<tvec3> &&v) : Model(move(v)) {}

shared_ptr<Model> Mesh::copy() const
{
    auto cp = make_shared<Mesh>();
    copy_to(cp);
    return cp;
}

const char *Mesh::type() const
{
    return "mesh";
}

size_t Mesh::to_obj(const string & path, const size_t offset) const 
{
    ofstream objfile(path, std::ios_base::app);
    objfile << "o Polygon" << offset << endl; 
    for(const auto & v: vertices)
        objfile << "v " << v.x << " " << v.y << " " << v.z << endl;

    for(size_t i = offset + 1; i < offset + 1 + vertices.size(); i += 3)
        objfile << "f " << i << " " << i + 1 << " " << i + 2 << endl;

    objfile.close();
    return vertices.size();
}

inline tvec3 tcentroid(const tvec3 triangle[3])
{
    tvec3 c = triangle[0] + triangle[1] + triangle[2];
    c /= 3.0;
    return c;
}

const tvec3 * Mesh::triangle(const size_t index) const
{
    return &(vertices[index * 3]);
}

const shared_ptr<Attribute> Mesh::attribute(const string & name)
{
    const auto it = attrib.find(name);
    if (it == attrib.end())
        throw runtime_error("The model is missing attribute " + name);
    return it->second;
}
