#include "graph.hpp"

Node::Node(const size_t id, const tfloat x, const tfloat y, const nlohmann::json & metadata)
{
    this->id = id;
    this->geometry = tvec3(x, y, 0.0f);
    this->metadata = metadata;
}

Edge::Edge(const size_t id, const size_t from, const size_t to, shared_ptr<Attribute> geometry, const nlohmann::json & metadata)
{
    this->id = id;
    this->from = from;
    this->to = to;
    this->geometry = geometry;
    this->metadata = metadata;
}

Graph::Graph()
{
}

void Graph::add_node(shared_ptr<Node> node)
{
    nodes[node->id] = node;
}

void Graph::add_edge(shared_ptr<Edge> edge)
{
    if (this->nodes.find(edge->from) == nodes.end())
        throw runtime_error("Node " + to_string(edge->from) + " not found");

    if (this->nodes.find(edge->to) == nodes.end())
        throw runtime_error("Node " + to_string(edge->to) + " not found");

    edges[edge->id] = edge;
    nodes[edge->from]->edges.push_back(edge);
    nodes[edge->to]->edges.push_back(edge);
}

int Graph::get_node_count() const
{
    return nodes.size();
}
int Graph::get_edge_count() const
{
    return edges.size();
}
