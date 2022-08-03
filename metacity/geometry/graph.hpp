#pragma once
#include "gltf/json.hpp"
#include "types.hpp"
#include "attribute.hpp"
#include <unordered_map>

using namespace std;

class Graph;


class Edge
{
public:
    Edge(const size_t id, const size_t from, const size_t to, const Attribute & geometry, const nlohmann::json & metadata);

protected:
    size_t id, from, to;
    Attribute geometry;
    nlohmann::json metadata;

    friend class Graph;
};


class Node
{
public:
    Node(const size_t id, const tfloat x, const tfloat y, const nlohmann::json & metadata);

protected:
    size_t id;
    tvec3 geometry;
    nlohmann::json metadata;
    vector<shared_ptr<Edge>> edges;

    friend class Graph;
};


class Graph
{
public:
    Graph();
    void add_node(const shared_ptr<Node> & node);
    void add_edge(const shared_ptr<Edge> & edge);

protected:
    unordered_map<size_t, shared_ptr<Node>> nodes;
    unordered_map<size_t, shared_ptr<Edge>> edges;
};