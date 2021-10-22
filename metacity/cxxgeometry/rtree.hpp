#pragma once
#include "types.hpp"
#include "bbox.hpp"
#include "polygons.hpp"

enum RTreeNodeType
{
    x = 0,
    y = 1,
    z = 2,
    leaf = 3
};

struct RTreeNode
{
    BBox bbox;
    uint8_t type;
};

struct RTreeLeafNode : public RTreeNode
{
    size_t index;
};

struct RTreeInternalNode : public RTreeNode
{
    shared_ptr<RTreeNode> L;
    shared_ptr<RTreeNode> R;
};

class RTree
{
public:
    RTree(const shared_ptr<SimpleMultiPolygon> smp);
    void range_query(const BBox &range, vector<size_t> & indices) const;
    void point_query(const tvec3 &point, vector<size_t> & indices) const;

protected:
    shared_ptr<RTreeNode> build(const BBox &box, const size_t start, const size_t end, const uint8_t axis);
    void rquery(const shared_ptr<RTreeNode> node, const BBox &range, vector<size_t> & indices) const;
    void pquery(const shared_ptr<RTreeNode> node, const tvec3 &point, vector<size_t> & indices) const;

    shared_ptr<RTreeNode> build_two_nodes(const BBox &box, const size_t start, const size_t end, const uint8_t axis);
    shared_ptr<RTreeNode> build_general(const BBox &box, const size_t start, const size_t end, const uint8_t axis);
    size_t classify(const tfloat split, BBox &left, BBox &right, const size_t start, const size_t end, const uint8_t axis);
    size_t handle_special_case(BBox &left, BBox &right, const size_t start, const size_t end, const uint8_t axis);
    shared_ptr<RTreeNode> root;

    vector<shared_ptr<RTreeNode>> nodes;
};
