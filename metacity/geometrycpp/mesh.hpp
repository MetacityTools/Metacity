#pragma once
#include "models.hpp"
#include <map>


using namespace std;

class RTree;
class LegoBuilder;

class TriangularMesh : public Model
{
public:
    TriangularMesh();
    TriangularMesh(const vector<tvec3> &v);
    TriangularMesh(const vector<tvec3> &&v);

    virtual shared_ptr<Model> copy() const override;
    virtual const char *type() const override;
    
    const tvec3 * triangle(const size_t index) const;
    const shared_ptr<Attribute> attribute(const string & name);

    virtual size_t to_obj(const string & path, const size_t offset) const override;

protected:
    friend class RTree;
    friend class LegoBuilder;
    friend class MeshOIDMapper;
};
