#include <stdexcept>
#include <fstream>
#include "points.hpp"

using namespace std;

//===============================================================================

Points::Points() : Model() {}
Points::Points(const vector<tvec3> & v) : Model(v) {}
Points::Points(const vector<tvec3> && v) : Model(move(v)) {}

shared_ptr<Model> Points::copy() const
{
    auto cp = make_shared<Points>();
    copy_to(cp);
    return cp;
}

const char * Points::type() const
{
    return "simplepoint";
}

size_t Points::to_obj(const string & path, const size_t offset) const 
{
    ofstream objfile(path, std::ios_base::app);
    objfile << "o Points" << offset << endl; 
    for(const auto & v: vertices)
        objfile << "v " << v.x << " " << v.y << " " << v.z << endl;
    objfile.close();
    return vertices.size();
}
