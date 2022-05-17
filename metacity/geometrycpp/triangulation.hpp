#pragma once
#include <vector>
#include "mapbox/earcut.hpp"
#include "types.hpp"


using namespace std;

class Triangulator {
public:
    Triangulator() {};
    void triangulate(const vector<vector<vector<tvec3>>> & in_polygon, vector<tvec3> & out_vertices);

protected:
    tvec3 compute_polygon_with_holes_normal(const vector<vector<tvec3>> & in_polygon) const;
    void project_along_normal(const vector<vector<tvec3>> & in_polygon, const tvec3 & normal);
    void to_output(const vector<vector<tvec3>> & polygon, vector<uint32_t> & indices, vector<tvec3> &out_vertices) const;
    
    vector<vector<tvec2>> projected;
};



