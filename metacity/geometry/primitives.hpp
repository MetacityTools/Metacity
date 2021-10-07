#include <vector>
#include <map>
#include <iostream>
#include "glm/glm.hpp"

using namespace std;

using tvec3 = glm::vec3;
using tvec2 = glm::vec2;
using tfloat = float;
using json = std::map<std::string, std::string>;


class Primitive
{
public:
    virtual ~Primitive();
    //virtual void transform() = 0;
    virtual json serialize() const = 0;

protected:
    vector<tfloat> vec_to_float(const vector<tvec3> & vec) const;
    vector<uint8_t> vec_to_unit8(const vector<tvec3> & vec) const;
    void append(vector<uint8_t> & vec, tfloat f) const;
    vector<tvec3> vertices;
};


class MultiPoint : public Primitive
{
public:
    void push_p2(const vector<tfloat> ivertices);
    void push_p3(const vector<tfloat> ivertices);
    vector<tfloat> contents() const;
    virtual json serialize() const override;

protected:
    vector<tvec3> points;
};


class MultiLine : public Primitive
{
public:
    void push_l2(const vector<tfloat> ivertices);
    void push_l3(const vector<tfloat> ivertices);
    vector<vector<tfloat>> contents() const;
    virtual json serialize() const override;
protected:
    vector<vector<tvec3>> lines;
};


class MultiPolygon : public Primitive
{
public:
    void push_p2(const vector<vector<tfloat>> ivertices);
    void push_p3(const vector<vector<tfloat>> ivertices);
    vector<vector<vector<tfloat>>> contents() const;
    virtual json serialize() const override;
protected:
    vector<vector<vector<tvec3>>> polygons;
};


