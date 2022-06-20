#include "attribute.hpp"
#include "triangulation.hpp"

Attribute::Attribute() : type(AttributeType::NONE) {}

void Attribute::allowedAttributeType(AttributeType type) {
    if (this->type != AttributeType::NONE || type != this->type) {
        throw runtime_error("Attribute type already set");
    }
    this->type = type;
}

void Attribute::push_point2D(const vector<tfloat> & ivertices)
{
    allowedAttributeType(AttributeType::POINT);

    if (ivertices.size() % tvec2::length())
        throw runtime_error("Unexpected number of elements in input array");

    for (size_t i = 0; i < ivertices.size(); i += tvec2::length())
        data.emplace_back(ivertices[i], ivertices[i + 1], 0);
}

void Attribute::push_point3D(const vector<tfloat> & ivertices)
{
    allowedAttributeType(AttributeType::POINT);

    if (ivertices.size() % tvec3::length())
        throw runtime_error("Unexpected number of elements in input array");

    for (size_t i = 0; i < ivertices.size(); i += tvec3::length())
        data.emplace_back(ivertices[i], ivertices[i + 1], ivertices[i + 2]);
}

void Attribute::push_line2D(const vector<tfloat> & ivertices)
{
    allowedAttributeType(AttributeType::SEGMENT);

    if (ivertices.size() % tvec2::length() || (ivertices.size() < tvec2::length() * 2))
        throw runtime_error("Unexpected number of elements in input array");

    for (size_t i = 1; i < ivertices.size() - 1; i += tvec2::length())
    {
        data.emplace_back(ivertices[i], ivertices[i + 1], 0);
        data.emplace_back(ivertices[i + 2], ivertices[i + 3], 0);
    }
}

void Attribute::push_line3D(const vector<tfloat> & ivertices)
{
    allowedAttributeType(AttributeType::SEGMENT);

    if (ivertices.size() % tvec3::length() || (ivertices.size() < tvec3::length() * 2))
        throw runtime_error("Unexpected number of elements in input array");

    for (size_t i = 1; i < ivertices.size() - 1; i += tvec3::length())
    {
        data.emplace_back(ivertices[i], ivertices[i + 1], ivertices[i + 2]);
        data.emplace_back(ivertices[i + 2], ivertices[i + 3], ivertices[i + 4]);
    }
}

void Attribute::push_polygon2D(const vector<vector<tfloat>> & ivertices)
{
    allowedAttributeType(AttributeType::POLYGON);

    vector<vector<tvec3>> polygon;
    for (const auto &iring : ivertices)
    {
        if (iring.size() % tvec2::length())
            throw runtime_error("Unexpected number of elements in input array");

        if ((iring.size() / tvec2::length()) < 3) // only a single point or a line
            continue;

        vector<tvec3> ring;
        for (size_t i = 0; i < iring.size(); i += tvec2::length())
            ring.emplace_back(iring[i], iring[i + 1], 0);
        polygon.emplace_back(move(ring));
    }

    triangulate(polygon, data);
}

void Attribute::push_polygon3D(const vector<vector<tfloat>> & ivertices)
{
    allowedAttributeType(AttributeType::POLYGON);

    vector<vector<tvec3>> polygon;
    for (const auto &iring : ivertices)
    {
        if (iring.size() % tvec3::length())
            throw runtime_error("Unexpected number of elements in input array");

        if ((iring.size() / tvec3::length()) < 3) // only a single point or a line
            continue;

        vector<tvec3> ring;
        for (size_t i = 0; i < iring.size(); i += tvec3::length())
            ring.emplace_back(iring[i], iring[i + 1], iring[i + 2]);
        polygon.emplace_back(move(ring));
    }

    triangulate(polygon, data);
}
