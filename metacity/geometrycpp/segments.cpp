#include <stdexcept>
#include <iostream>
#include <fstream>
#include "segments.hpp"

//===============================================================================

Segments::Segments() : Model() {}
Segments::Segments(const vector<tvec3> &v) : Model(v) {}
Segments::Segments(const vector<tvec3> &&v) : Model(move(v)) {}

shared_ptr<Model> Segments::copy() const
{
    auto cp = make_shared<Segments>();
    copy_to(cp);
    return cp;
}

const char *Segments::type() const
{
    return "simpleline";
}

inline tvec3 lcentroid(const tvec3 line[2])
{
    tvec3 c = line[0] + line[1];
    c /= 2.0;
    return c;
}

void Segments::add_attribute(const string &name, const uint32_t value)
{
    auto attr = make_shared<TAttribute<uint32_t>>();
    attr->clear();
    attr->fill(value, vertices.size() / 2);
    attrib[name] = attr;
}

size_t Segments::to_obj(const string &path, const size_t offset) const
{
    ofstream objfile(path, std::ios_base::app);
    objfile << "o Line" << offset << endl;
    for (const auto &v : vertices)
        objfile << "v " << v.x << " " << v.y << " " << v.z << endl;

    for (size_t i = offset + 1; i < offset + 1 + vertices.size(); i += 2)
        objfile << "l " << i << " " << i + 1 << endl;

    objfile.close();
    return vertices.size();
}