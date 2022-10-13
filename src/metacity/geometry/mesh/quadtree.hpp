#include "../types.hpp"
#include "model.hpp"
#include "../progress.hpp"


struct MetadataAggregate {
    unordered_map<string, unordered_map<string, size_t>> str;
    unordered_map<string, vector<tfloat>> num;
};


class QuadTreeLevel {
public:
    QuadTreeLevel(size_t depth, BBox border);
    void add_models(const vector<shared_ptr<Model>> & models, size_t max_depth, Progress & progress);
    nlohmann::json to_json(const string & dirname, size_t yield_models_at_level, Progress & progress) const; 

protected:
    static size_t gen_id() { return id_counter++; }
    static size_t id_counter;
    
    shared_ptr<QuadTreeLevel> init_child(BBox border, size_t max_depth, Progress & bar);
    
    bool is_leaf() const;
    bool is_empty() const;
    void to_gltf(const string & filename) const;
    void aggregate_metadata();
    void consolidate_metadata(const MetadataAggregate & metadata);


    size_t id;
    size_t depth;
    BBox border;
    shared_ptr<QuadTreeLevel> ne, se, sw, nw;
    nlohmann::json metadata;
    vector<shared_ptr<Model>> models;
};


class QuadTree {
public:
    QuadTree(const vector<shared_ptr<Model>> & models, size_t max_depth = 0);
    void to_json(const string & dirname, size_t yield_models_at_level) const;
protected:
    shared_ptr<QuadTreeLevel> root;
};