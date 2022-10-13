#include <fstream>
#include "quadtree.hpp"
#include "../progress.hpp"

using json = nlohmann::json;
size_t QuadTreeLevel::id_counter = 0;

QuadTree::QuadTree(const vector<shared_ptr<Model>> &models, size_t max_depth)
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

void QuadTree::to_json(const string &dirname, size_t yield_models_at_level) const
{
    if (root)
    {
        Progress bar("QuadTree to json");
        auto meta = root->to_json(dirname, yield_models_at_level, bar);
        ofstream metafile(dirname + "/meta.json");
        metafile << meta.dump(-1);
        metafile.close();
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
    return models.empty();
}

void QuadTreeLevel::add_models(const vector<shared_ptr<Model>> &models_, size_t max_depth, Progress & bar)
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

shared_ptr<QuadTreeLevel> QuadTreeLevel::init_child(BBox border, size_t max_depth, Progress & bar)
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

json QuadTreeLevel::to_json(const string &dirname, size_t yield_models_at_level, Progress & bar) const
{
    const string base_name = "quad" + to_string(depth) + "_" + to_string(id);

    json out = {
        {"metadata", metadata},
        {"z", {border.min.z, border.max.z}}};

    if (depth == 0)
    {
        out["border"] = {
            {"min", {border.min.x, border.min.y}},
            {"max", {border.max.x, border.max.y}}};
    }

    if ((is_leaf() && depth < yield_models_at_level) || depth == yield_models_at_level - 1)
    {
        const string filename = dirname + "/" + base_name + ".glb";
        out["file"] = base_name + ".glb";
        out["size"] = models.size();
        to_gltf(filename);
    }

    if (ne != nullptr)
        out["ne"] = ne->to_json(dirname, yield_models_at_level, bar);
    if (se != nullptr)
        out["se"] = se->to_json(dirname, yield_models_at_level, bar);
    if (sw != nullptr)
        out["sw"] = sw->to_json(dirname, yield_models_at_level, bar);
    if (nw != nullptr)
        out["nw"] = nw->to_json(dirname, yield_models_at_level, bar);

    bar.update();
    return out;
}

void QuadTreeLevel::to_gltf(const string &filename) const
{
    tinygltf::Model gltf_model;
    tinygltf::Asset asset;
    asset.version = "2.0";
    asset.generator = "Metacity";
    gltf_model.asset = asset;

    for (auto &model : models)
    {
        if (inside(border, model->get_centroid()))
            model->to_gltf(gltf_model);
    }

    tinygltf::TinyGLTF gltf;
    gltf.SetStoreOriginalJSONForExtrasAndExtensions(true);
    gltf.WriteGltfSceneToFile(&gltf_model, filename, true, true, true, true);
}