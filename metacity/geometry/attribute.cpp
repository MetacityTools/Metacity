#include "attribute.hpp"
#include "triangulation.hpp"

Attribute::Attribute() : type(AttributeType::NONE) {}


void Attribute::allowedAttributeType(AttributeType type) {
    if (this->type != AttributeType::NONE && this->type != type) {
        throw runtime_error("Attribute type already set to " + to_string(this->type));
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

void Attribute::fill_normal_triangle(const tvec3 & normal)
{
    allowedAttributeType(AttributeType::NORMAL);
    data.push_back(normal);
    data.push_back(normal);
    data.push_back(normal);
}

tvec3 Attribute::vmin() const
{
    if (data.empty())
        return tvec3(INFINITY);

    tvec3 min = data[0];
    for (const auto &v : data)
        min = glm::min(min, v);
    return min;
}

tvec3 Attribute::vmax() const
{
    if (data.empty())
        return tvec3(-INFINITY);

    tvec3 max = data[0];
    for (const auto &v : data)
        max = glm::max(max, v);
    return max;
}

tvec3 Attribute::sum() const
{
    tvec3 sum = tvec3(0);
    for (const auto &v : data)
        sum += v;
    return sum;
}

size_t Attribute::size() const
{
    return data.size();
}

shared_ptr<Attribute> Attribute::clone() const
{
    auto clone = make_shared<Attribute>();
    clone->type = type;
    clone->data = data;
    return clone;
}

void Attribute::merge(shared_ptr<Attribute> other)
{
    if (type != other->type)
        throw runtime_error("Cannot merge attributes of different types");
    data.insert(data.end(), other->data.begin(), other->data.end());
}

void Attribute::to_gltf(tinygltf::Model & model, AttributeType & type_, int & accessor_index) const
{
    int buffer_index, buffer_size, buffer_view_index;
    to_gltf_buffer(model, buffer_index, buffer_size);
    to_gltf_buffer_view(model, buffer_index, buffer_size, buffer_view_index);
    to_gltf_accessor(model, buffer_view_index, accessor_index);
    type_ = type;
}

void Attribute::to_gltf_buffer(tinygltf::Model & model, int & buffer_index, int & size) const
{
    tinygltf::Buffer buffer;
    size = data.size() * sizeof(tvec3);
    buffer.data = vector<unsigned char>(size);
    memcpy(buffer.data.data(), data.data(), buffer.data.size());
    model.buffers.push_back(buffer);
    buffer_index = model.buffers.size() - 1;
}

void Attribute::to_gltf_buffer_view(tinygltf::Model & model, const int buffer_index, const int size, int & buffer_view_index) const
{
    tinygltf::BufferView bufferView;
    bufferView.buffer = buffer_index;
    bufferView.byteLength = size;
    bufferView.byteOffset = 0;
    bufferView.target = TINYGLTF_TARGET_ARRAY_BUFFER;
    model.bufferViews.push_back(bufferView);
    buffer_view_index = model.bufferViews.size() - 1;
}

void Attribute::to_gltf_accessor(tinygltf::Model & model, const int buffer_view_index, int & accessor_index) const
{
    tinygltf::Accessor accessor;
    accessor.bufferView = buffer_view_index;
    accessor.byteOffset = 0;
    accessor.componentType = TINYGLTF_COMPONENT_TYPE_FLOAT;
    accessor.count = data.size();
    accessor.type = TINYGLTF_TYPE_VEC3;
    tvec3 min = vmin();
    tvec3 max = vmax();
    accessor.minValues = {min.x, min.y, min.z};
    accessor.maxValues = {max.x, max.y, max.z};
    model.accessors.push_back(accessor);
    accessor_index = model.accessors.size() - 1;
}

//===============================================================================

void Attribute::from_gltf(const tinygltf::Model & model, AttributeType type_, const int accessor_index)
{
    attr_type_check(model, accessor_index);
    const tinygltf::Accessor & accessor = model.accessors[accessor_index];
    const tinygltf::BufferView & bufferView = model.bufferViews[accessor.bufferView];
    const tinygltf::Buffer & buffer = model.buffers[bufferView.buffer];
    type = type_;

    data.resize(accessor.count);
    memcpy(data.data(), buffer.data.data() + bufferView.byteOffset + accessor.byteOffset, bufferView.byteLength);
}

//===============================================================================
// Checks

void Attribute::attr_type_check(const tinygltf::Model & model, const int accessor_index) const
{
    const tinygltf::Accessor & accessor = model.accessors[accessor_index];
    const tinygltf::BufferView & bufferView = model.bufferViews[accessor.bufferView];
    //const tinygltf::Buffer & buffer = model.buffers[bufferView.buffer];

    if (accessor.type != TINYGLTF_TYPE_VEC3)
        throw runtime_error("Attribute type mismatch");
    if (accessor.componentType != TINYGLTF_COMPONENT_TYPE_FLOAT)
        throw runtime_error("Attribute component type mismatch");
    if (bufferView.target != TINYGLTF_TARGET_ARRAY_BUFFER)
        throw runtime_error("Attribute buffer view target mismatch");
    if (bufferView.byteLength % sizeof(tvec3) != 0)
        throw runtime_error("Attribute buffer view size mismatch");

    if (accessor.minValues.size() != 3)
        throw runtime_error("Attribute min values size mismatch");
    if (accessor.maxValues.size() != 3)
        throw runtime_error("Attribute max values size mismatch");
    if (accessor.minValues[0] > accessor.maxValues[0])
        throw runtime_error("Attribute min values out of range");
}

