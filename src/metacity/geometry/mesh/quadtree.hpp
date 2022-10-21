#include "../types.hpp"
#include "model.hpp"
#include "layer.hpp"
#include "../progress.hpp"


struct MetadataAggregate {
    unordered_map<string, unordered_map<string, tfloat>> str;
    unordered_map<string, unordered_map<tfloat, tfloat>> num;
};

enum class MetadataMode : uint8_t
{
    AVERAGE = 0,
    MAX_AREA = 1,
};


class QuadTreeLevel {
public:
    QuadTreeLevel(size_t depth, BBox border);
    void add_models(const vector<shared_ptr<Model>> & models, MetadataMode num_values_mode, size_t max_depth, Progress & progress);
    nlohmann::json to_json(const string & dirname, size_t yield_models_at_level, bool store_metadata, Progress & progress) const; 
    void grid_layout(const string & dirname, size_t yield_models_at_level, nlohmann::json  & layout, Progress & progress) const;
    void quad_merge(size_t merge_models_at_level);
    void filter_metadata(const vector<string> & keys);
protected:
    static size_t gen_id() { return id_counter++; }
    static size_t id_counter;
    
    shared_ptr<QuadTreeLevel> init_child(BBox border, MetadataMode num_values_mode, size_t max_depth, Progress & bar);
    
    bool is_leaf() const;
    bool is_empty() const;
    void to_gltf(const string & filename) const;
    void process_metadata(MetadataMode num_values_mode);

    //Average or max occurance
    void aggregate_metadata(MetadataMode num_values_mode);
    void consolidate_aggregated_metadata(const MetadataAggregate & metadata, MetadataMode num_values_mode);
    string glb_filename() const;


    size_t id;
    size_t depth;
    BBox border;
    shared_ptr<QuadTreeLevel> ne, se, sw, nw;
    nlohmann::json metadata;
    vector<shared_ptr<Model>> models;
};


class QuadTree {
public:
    QuadTree(const vector<shared_ptr<Model>> & models, MetadataMode num_values_mode = MetadataMode::AVERAGE, size_t max_depth = 10);
    QuadTree(shared_ptr<Layer> layer, MetadataMode num_values_mode = MetadataMode::AVERAGE, size_t max_depth = 10);
    void merge_at_level(size_t merge_models_at_level);
    void filter_metadata(const vector<string> & keys);
    void to_json(const string & dirname, size_t yield_models_at_level, bool store_metadata = true) const;
protected:
    void init(const vector<shared_ptr<Model>> & models, MetadataMode num_values_mode, size_t max_depth);
    shared_ptr<QuadTreeLevel> root;
};