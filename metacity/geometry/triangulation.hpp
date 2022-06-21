#pragma once
#include <vector>
#include "mapbox/earcut.hpp"
#include "types.hpp"

using namespace std;

void triangulate(const vector<vector<tvec3>> & in_polygon, vector<tvec3> & out_vertices);

