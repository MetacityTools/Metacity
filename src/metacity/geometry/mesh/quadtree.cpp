#include <fstream>
#include "quadtree.hpp"
#include "../progress.hpp"
#include "modifiers.hpp"

using json = nlohmann::json;
size_t QuadTreeLevel::id_counter = 0;

QuadTree::QuadTree(const vector<shared_ptr<Model>> &models, size_t max_depth)
{
    init(models, max_depth);
}

QuadTree::QuadTree(shared_ptr<Layer> layer, size_t max_depth)
{
    const auto &models = layer->get_models();
    init(models, max_depth);
}

void QuadTree::init(const vector<shared_ptr<Model>> &models, size_t max_depth)
{
    if (models.size() == 0)
    {
        throw runtime_error("QuadTree: no models");
    }

    BBox root_bbox = models[0]->get_bbox();
    for (size_t i = 1; i < models.size(); i++)
        extend(root_bbox, models[i]->get_bbox());

    root_bbox = toEqualXY(root_bbox);
    root = make_shared<QuadTreeLevel>(0, root_bbox);

    Progress bar("QuadTree build");
    root->add_models(models, max_depth, bar);
}

void QuadTree::merge_at_level(size_t merge_models_at_level)
{
    if (root)
        root->quad_merge(merge_models_at_level);
}

void QuadTree::to_json(const string &dirname, size_t yield_models_at_level, bool store_metadata) const
{
    if (root)
    {
        Progress bar("QuadTree to json");
        auto meta = root->to_json(dirname, yield_models_at_level, store_metadata, bar);
        ofstream metafile(dirname + "/meta.json");
        metafile << meta.dump(-1);
        metafile.close();
    }

    if (root)
    {
        Progress bar("QuadTree grid layout");
        json layout;
        root->grid_layout(dirname, yield_models_at_level, layout, bar);
        ofstream layoutfile(dirname + "/layout.json");
        layoutfile << layout.dump(-1);
        layoutfile.close();
    }
}

QuadTreeLevel::QuadTreeLevel(size_t depth_, BBox border_)
    : id(gen_id()), depth(depth_), border(border_), ne(nullptr), se(nullptr), sw(nullptr), nw(nullptr)
{
}

bool QuadTreeLevel::is_leaf() const
{
    return ne == nullptr && se == nullptr && sw == nullptr && nw == nullptr;
}
bool QuadTreeLevel::is_empty() const
{
    return models.empty() || border.min.z == INFINITY || border.max.z == -INFINITY;
}

void QuadTreeLevel::add_models(const vector<shared_ptr<Model>> &models_, size_t max_depth, Progress &bar)
{
    // reset the z.coord of the bbox
    border.min.z = INFINITY;
    border.max.z = -INFINITY;

    for (auto model : models_)
    {
        BBox model_box = model->get_bbox(true);
        if (overlaps(border, model_box))
        {
            // add model to this level
            models.push_back(model);
            // adjust z to fut model box
            border.min.z = min(border.min.z, model_box.min.z);
            border.max.z = max(border.max.z, model_box.max.z);
        }
    }

    // add models to subtrees
    if (!is_empty())
    {
        if (depth < max_depth)
        {
            auto center = border.centroid();
            ne = init_child(BBox{tvec3(center.x, center.y, border.min.z), border.max}, max_depth, bar);
            se = init_child(BBox{tvec3(center.x, border.min.y, border.min.z), tvec3(border.max.x, center.y, border.max.z)}, max_depth, bar);
            sw = init_child(BBox{border.min, tvec3(center.x, center.y, border.max.z)}, max_depth, bar);
            nw = init_child(BBox{tvec3(border.min.x, center.y, border.min.z), tvec3(center.x, border.max.y, border.max.z)}, max_depth, bar);
        }
    }

    // sort out metadata
    if (!is_empty())
    {
        aggregate_metadata();
        bar.update();
    }
}

shared_ptr<QuadTreeLevel> QuadTreeLevel::init_child(BBox border, size_t max_depth, Progress &bar)
{
    auto child = make_shared<QuadTreeLevel>(depth + 1, border);
    child->add_models(models, max_depth, bar);
    if (child->is_empty())
        return nullptr;
    return child;
}

void QuadTreeLevel::aggregate_metadata()
{
    MetadataAggregate metadata_;
    for (auto model : models)
    {
        const json model_meta = model->get_metadata();
        for (auto it = model_meta.begin(); it != model_meta.end(); ++it)
        {

            if (it.value().is_number())
            {
                const tfloat value = it.value();
                if (metadata_.num.find(it.key()) == metadata_.num.end())
                {
                    metadata_.num[it.key()] = vector<tfloat>();
                }
                metadata_.num[it.key()].push_back(value);
            }

            if (it.value().is_string())
            {
                const string &str = it.value();
                if (metadata_.str.find(it.key()) == metadata_.str.end())
                {
                    metadata_.str[it.key()] = unordered_map<string, size_t>();
                }

                auto &coutner = metadata_.str[it.key()];
                if (coutner.find(it.value()) == coutner.end())
                {
                    coutner[str] = 0;
                }

                coutner[str]++;
            }
        }
    }

    consolidate_metadata(metadata_);
}

void QuadTreeLevel::consolidate_metadata(const MetadataAggregate &metadata_)
{
    for (auto it = metadata_.num.begin(); it != metadata_.num.end(); ++it)
    {
        const string &key = it->first;
        const vector<tfloat> &values = it->second;
        tfloat sum = 0;
        for (auto value : values)
        {
            sum += value;
        }
        metadata[key] = sum / values.size();
    }

    for (auto it = metadata_.str.begin(); it != metadata_.str.end(); ++it)
    {
        const string &key = it->first;
        const unordered_map<string, size_t> &values = it->second;
        size_t max_count = 0;
        string max_str;
        for (auto it2 = values.begin(); it2 != values.end(); ++it2)
        {
            if (it2->second > max_count)
            {
                max_count = it2->second;
                max_str = it2->first;
            }
        }
        metadata[key] = max_str;
    }
}

string QuadTreeLevel::glb_filename() const
{
    return "quad" + to_string(depth) + "_" + to_string(id) + ".glb";
}

json QuadTreeLevel::to_json(const string &dirname, size_t yield_models_at_level, bool store_metadata, Progress &bar) const
{
    const string glb_name = glb_filename();

    json out = {
        {"z", {border.min.z, border.max.z}}};

    if (store_metadata)
        out["metadata"] = metadata;

    if (depth == 0)
    {
        out["border"] = {
            {"min", {border.min.x, border.min.y}},
            {"max", {border.max.x, border.max.y}}};
    }

    if ((is_leaf() && depth < yield_models_at_level) || depth == yield_models_at_level - 1)
    {
        const string filename = dirname + "/" + glb_name;
        out["file"] = glb_name;
        out["size"] = models.size();
        to_gltf(filename);
    }

    if (ne != nullptr)
        out["ne"] = ne->to_json(dirname, yield_models_at_level, store_metadata, bar);
    if (se != nullptr)
        out["se"] = se->to_json(dirname, yield_models_at_level, store_metadata, bar);
    if (sw != nullptr)
        out["sw"] = sw->to_json(dirname, yield_models_at_level, store_metadata, bar);
    if (nw != nullptr)
        out["nw"] = nw->to_json(dirname, yield_models_at_level, store_metadata, bar);

    bar.update();
    return out;
}

void QuadTreeLevel::grid_layout(const string &dirname, size_t yield_models_at_level, json &layout, Progress &bar) const
{

    if (depth == 0)
    {
        const size_t p = (1 << (yield_models_at_level - 1));
        layout["tileWidth"] = (border.max.x - border.min.x) / p;
        layout["tileHeight"] = (border.max.y - border.min.y) / p;
        layout["tiles"] = json::array();
    }

    if ((is_leaf() && depth < yield_models_at_level) || depth == yield_models_at_level - 1)
    {

        const tfloat tw = layout["tileWidth"].get<tfloat>();
        const tfloat th = layout["tileHeight"].get<tfloat>();

        const int x = floor(border.min.x / tw);
        const int y = floor(border.min.y / th);

        json tile;
        tile["x"] = x;
        tile["y"] = y;
        tile["file"] = glb_filename();
        tile["size"] = models.size();
        layout["tiles"].push_back(tile);
    }

    if (ne != nullptr)
        ne->grid_layout(dirname, yield_models_at_level, layout, bar);
    if (se != nullptr)
        se->grid_layout(dirname, yield_models_at_level, layout, bar);
    if (sw != nullptr)
        sw->grid_layout(dirname, yield_models_at_level, layout, bar);
    if (nw != nullptr)
        nw->grid_layout(dirname, yield_models_at_level, layout, bar);

    bar.update();
}

void QuadTreeLevel::quad_merge(size_t merge_models_at_level)
{
    if ((is_leaf() && depth < merge_models_at_level) || depth == merge_models_at_level - 1)
    {

        // filter nodels inside
        vector<shared_ptr<Model>> models_;
        for (auto &model : models)
        {
            if (inside(border, model->get_centroid()))
                models_.push_back(model);
        }

        auto model = modifiers::merge_models(models_);
        models.clear();
        models.push_back(model);
    }
    else
    {
        if (ne != nullptr)
            ne->quad_merge(merge_models_at_level);
        if (se != nullptr)
            se->quad_merge(merge_models_at_level);
        if (sw != nullptr)
            sw->quad_merge(merge_models_at_level);
        if (nw != nullptr)
            nw->quad_merge(merge_models_at_level);
    }
}

void QuadTreeLevel::to_gltf(const string &filename) const
{
    tinygltf::Model gltf_model;
    tinygltf::Asset asset;
    asset.version = "2.0";
    asset.generator = "Metacity";
    gltf_model.asset = asset;

    if (models.size() == 1)
    {
        auto model = models[0];
        model->to_gltf(gltf_model);
    }
    else
    {
        for (auto &model : models)
        {
            if (inside(border, model->get_centroid()))
                model->to_gltf(gltf_model);
        }
    }

    tinygltf::TinyGLTF gltf;
    gltf.SetStoreOriginalJSONForExtrasAndExtensions(true);
    gltf.WriteGltfSceneToFile(&gltf_model, filename, true, true, true, true);
}