#include <stdexcept>
#include <unordered_map>
#include <fstream>
#include "points.hpp"

using namespace std;

//===============================================================================

PointCloud::PointCloud() : Model() {}
PointCloud::PointCloud(const vector<tvec3> & v) : Model(v) {}
PointCloud::PointCloud(const vector<tvec3> && v) : Model(move(v)) {}

shared_ptr<Model> PointCloud::copy() const
{
    auto cp = make_shared<PointCloud>();
    copy_to(cp);
    return cp;
}

const char * PointCloud::type() const
{
    return "simplepoint";
}

size_t PointCloud::to_obj(const string & path, const size_t offset) const 
{
    ofstream objfile(path, std::ios_base::app);
    objfile << "o PointCloud" << offset << endl; 
    for(const auto & v: vertices)
        objfile << "v " << v.x << " " << v.y << " " << v.z << endl;
    objfile.close();
    return vertices.size();
}
