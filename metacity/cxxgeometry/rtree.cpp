#include "rtree.hpp"

//===============================================================================

void for_triangle(const tvec3 t[3], BBox & box)
{
    box.min.x = min(t[0].x, min(t[1].x, t[2].x));
    box.min.y = min(t[0].y, min(t[1].y, t[2].y));
    box.min.z = min(t[0].z, min(t[1].z, t[2].z));
    box.max.x = max(t[0].x, max(t[1].x, t[2].x));
    box.max.y = max(t[0].y, max(t[1].y, t[2].y));
    box.max.z = max(t[0].z, max(t[1].z, t[2].z));
}

void for_line(const tvec3 l[2], BBox & box)
{
    box.min.x = min(l[0].x, l[1].x);
    box.min.y = min(l[0].y, l[1].y);
    box.min.z = min(l[0].z, l[1].z);
    box.max.x = max(l[0].x, l[1].x);
    box.max.y = max(l[0].y, l[1].y);
    box.max.z = max(l[0].z, l[1].z);
}

void for_bboxes(const BBox &b1, const BBox &b2, BBox & outb)
{
    outb.min.x = min(b1.min.x, b2.min.x);
    outb.min.y = min(b1.min.y, b2.min.y);
    outb.min.z = min(b1.min.z, b2.min.z);
    outb.max.x = max(b1.max.x, b2.max.x);
    outb.max.y = max(b1.max.y, b2.max.y);
    outb.max.z = max(b1.max.z, b2.max.z);
}

bool overlaps(const BBox &b1, const BBox &b2)
{
    // If one rectangle is on left side of other               or above
    return !((b1.min.x >= b2.max.x || b2.min.x >= b1.max.x) || (b1.min.y >= b2.max.y || b2.min.y >= b1.max.y));
}

bool inside(const BBox &b, const tvec3 &p)
{
    return ((b.min.x <= p.x) && (p.x >= b.max.x)) && ((b.min.y <= p.y) && (p.y >= b.max.y));
}

void set_empty(BBox &box)
{
    box.min = tvec3(FLT_MAX);
    box.max = tvec3(-FLT_MAX);
}

void extend(BBox &b1, const BBox &b2)
{
    b1.min.x = min(b1.min.x, b2.min.x);
    b1.min.y = min(b1.min.y, b2.min.y);
    b1.min.z = min(b1.min.z, b2.min.z);
    b1.max.x = max(b1.max.x, b2.max.x);
    b1.max.y = max(b1.max.y, b2.max.y);
    b1.max.z = max(b1.max.z, b2.max.z);
}

tfloat midpoint(const BBox &b1, uint8_t axis)
{
    return (b1.min[axis] + b1.max[axis]) / 2;
}

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