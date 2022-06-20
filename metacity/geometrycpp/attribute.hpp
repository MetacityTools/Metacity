#pragma once
#include <vector>
#include "types.hpp"

using namespace std;


enum AttributeType {
    NONE,
    POINT,
    SEGMENT,
    POLYGON
};


class Attribute {
public:
    Attribute();
    void push_point2D(const vector<tfloat> & ivertices);
    void push_point3D(const vector<tfloat> & ivertices);
    void push_line2D(const vector<tfloat> & ivertices);
    void push_line3D(const vector<tfloat> & ivertices); 
    void push_polygon2D(const vector<vector<tfloat>> & ivertices);
    void push_polygon3D(const vector<vector<tfloat>> & ivertices); 

protected:
    void allowedAttributeType(AttributeType type);

    vector<tvec3> data;
    AttributeType type;
};


