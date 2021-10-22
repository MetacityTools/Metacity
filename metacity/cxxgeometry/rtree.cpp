#include "rtree.hpp"

//===============================================================================

RTree::RTree(const shared_ptr<SimpleMultiPolygon> smp)
{

    BBox main;
    set_empty(main);
    for (size_t i = 0, j = 0; i < smp->vertices.size(); i += 3, ++j)
    {
        auto node = make_shared<RTreeLeafNode>();
        for_triangle(&(smp->vertices[i]), node->bbox);
        extend(main, node->bbox);
        node->index = j;
        node->type = RTreeNodeType::leaf;
        nodes.push_back(node);
    }

    root = build(main, 0, nodes.size(), 0);
}

shared_ptr<RTreeNode> RTree::build_two_nodes(const BBox &box, const size_t start, const size_t end, const uint8_t axis)
{
    auto node = make_shared<RTreeInternalNode>();
    node->type = axis;
    node->bbox = box;
    const auto l = nodes[start];
    const auto r = nodes[start + 1];
    for_bboxes(l->bbox, r->bbox, node->bbox);
    const tvec3 lc = l->bbox.centroid();
    const tvec3 rc = r->bbox.centroid();

    if (lc[axis] < rc[axis])
    {
        node->L = l;
        node->R = r;
    }
    else
    {
        node->L = r;
        node->R = l;
    }
    return node;
}

size_t RTree::classify(const tfloat split, BBox &left, BBox &right, const size_t start, const size_t end, const uint8_t axis)
{
    set_empty(left);
    set_empty(right);

    tfloat mid;
    size_t firstRight = start;
    for (size_t i = start; i < end; i++)
    {
        mid = midpoint(nodes[i]->bbox, axis);
        if (mid >= split)
        {
            extend(right, nodes[i]->bbox);
        }
        else
        {
            extend(left, nodes[i]->bbox);
            swap(nodes[i], nodes[firstRight]);
            ++firstRight;
        }
    }

    return firstRight;
}

size_t RTree::handle_special_case(BBox &left, BBox &right, const size_t start, const size_t end, const uint8_t axis)
{
    set_empty(left);
    set_empty(right);

    tfloat minMid = FLT_MAX;
    tfloat mid;

    for (size_t i = start; i < end; i++)
    {
        mid = midpoint(nodes[i]->bbox, axis);
        if (mid < minMid)
            minMid = mid, swap(nodes[i], nodes[start]);
    }

    extend(left, nodes[start]->bbox);
    for (size_t i = start + 1; i < end; i++)
        extend(right, nodes[i]->bbox);

    return start + 1;
}

shared_ptr<RTreeNode> RTree::build_general(const BBox &box, const size_t start, const size_t end, const uint8_t axis)
{
    auto node = make_shared<RTreeInternalNode>();
    node->bbox = box;
    BBox left, right;
    tfloat split = midpoint(box, axis);
    size_t firstRight = classify(split, left, right, start, end, axis);

    // maybe?
    if (start == firstRight || end == firstRight)
        firstRight = handle_special_case(left, right, start, end, axis);

    uint8_t naxis = (axis + 1) % 2;
    node->L = build(left, start, firstRight, naxis);
    node->R = build(right, firstRight, end, naxis);
    return node;
}

shared_ptr<RTreeNode> RTree::build(const BBox &box, const size_t start, const size_t end, const uint8_t axis)
{
    size_t size = end - start;
    if (size == 1)
        return nodes[start];
    if (size == 2)
        return build_two_nodes(box, start, end, axis);

    return build_general(box, start, end, axis);
}

void RTree::range_query(const BBox &range, vector<size_t> & out) const
{
    if (overlaps(root->bbox, range))
        rquery(root, range, out);
}

void RTree::point_query(const tvec3 &point, vector<size_t> & out) const
{
    if (inside(root->bbox, point))
        pquery(root, point, out);
}

void RTree::rquery(const shared_ptr<RTreeNode> node, const BBox &range, vector<size_t> & out) const
{
    if (node->type == RTreeNodeType::leaf)
    {
        const auto leaf = static_pointer_cast<RTreeLeafNode>(node);
        out.emplace_back(leaf->index);
    }
    else
    {
        const auto internal = static_pointer_cast<RTreeInternalNode>(node);
        if (overlaps(range, internal->L->bbox))
            rquery(internal->L, range, out);
        if (overlaps(range, internal->R->bbox))
            rquery(internal->R, range, out);
    }
}


void RTree::pquery(const shared_ptr<RTreeNode> node, const tvec3 &point, vector<size_t> & out) const
{
    if (node->type == RTreeNodeType::leaf)
    {
        const auto leaf = static_pointer_cast<RTreeLeafNode>(node);
        out.emplace_back(leaf->index);
    }
    else
    {
        const auto internal = static_pointer_cast<RTreeInternalNode>(node);
        if (inside(internal->L->bbox, point))
            pquery(internal->L, point, out);
        if (inside(internal->R->bbox, point))
            pquery(internal->R, point, out);
    }
}