#include <fstream>
#include "quadtree.hpp"
#include "../progress.hpp"
#include "modifiers.hpp"

using json = nlohmann::json;
size_t QuadTreeLevel::id_counter = 0;

QuadTree::QuadTree(const vector<shared_ptr<Model>> &models, MetadataMode num_values_mode, size_t max_depth)
{
    init(models, num_values_mode, max_depth);
}

QuadTree::QuadTree(shared_ptr<Layer> layer, MetadataMode num_values_mode, size_t max_depth)
{
    const auto &models = layer->get_models();
    init(models, num_values_mode, max_depth);
}

void QuadTree::init(const vector<shared_ptr<Model>> &models, MetadataMode num_values_mode, size_t max_depth)
{
    if (models.size() == 0)
    {
        throw runtime_error("QuadTree: no models");
    }

    BBox root_bbox = models[0]->get_bbox();
    for (size_t i = 1; i < models.size(); i++)
        root_bbox.extend(models[i]->get_bbox());

    root_bbox.toEqualXY();
    root = make_shared<QuadTreeLevel>(0, root_bbox);

    Progress bar("QuadTree build");
    root->add_models(models, num_values_mode, max_depth, bar);
}

void QuadTree::merge_at_level(size_t merge_models_at_level)
{
    if (root)
        root->quad_merge(merge_models_at_level);
}

void QuadTree::filter_metadata(const vector<string> &keys)
{
    if (root)
        root->filter_metadata(keys);
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

void QuadTreeLevel::add_models(const vector<shared_ptr<Model>> &models_, MetadataMode num_values_mode, size_t max_depth, Progress &bar)
{
    // reset the z.coord of the bbox
    border.min.z = INFINITY;
    border.max.z = -INFINITY;

    size_t i = 0;
    for (auto model : models_)
    {
        if (model->overlaps(border))
        {
            BBox model_box = model->get_bbox(true);
            // add model to this level
            models.push_back(model);
            // adjust z to fit model box
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
            ne = init_child(BBox(tvec3(center.x, center.y, border.min.z), border.max), num_values_mode, max_depth, bar);
            se = init_child(BBox(tvec3(center.x, border.min.y, border.min.z), tvec3(border.max.x, center.y, border.max.z)), num_values_mode, max_depth, bar);
            sw = init_child(BBox(border.min, tvec3(center.x, center.y, border.max.z)), num_values_mode, max_depth, bar);
            nw = init_child(BBox(tvec3(border.min.x, center.y, border.min.z), tvec3(center.x, border.max.y, border.max.z)), num_values_mode, max_depth, bar);
        }
    }

    // sort out metadata
    if (!is_empty())
    {
        process_metadata(num_values_mode);
        bar.update();
    }
}

shared_ptr<QuadTreeLevel> QuadTreeLevel::init_child(BBox border, MetadataMode num_values_mode, size_t max_depth, Progress &bar)
{
    auto child = make_shared<QuadTreeLevel>(depth + 1, border);
    child->add_models(models, num_values_mode, max_depth, bar);
    if (child->is_empty())
        return nullptr;
    return child;
}

void QuadTreeLevel::process_metadata(MetadataMode num_values_mode)
{
    //TODO refactor
    aggregate_metadata(num_values_mode);
}

void QuadTreeLevel::aggregate_metadata(MetadataMode num_values_mode)
{
    MetadataAggregate metadata_;
    for (auto model : models)
    {
        const json model_meta = model->get_metadata();
        for (auto it = model_meta.begin(); it != model_meta.end(); ++it)
        {

            if (it.value().is_number())
            {
                const tfloat num = it.value();
                if (metadata_.num.find(it.key()) == metadata_.num.end())
                {
                    metadata_.num[it.key()] = unordered_map<tfloat, tfloat>();
                }

                auto &coutner = metadata_.num[it.key()];
                if (coutner.find(it.value()) == coutner.end())
                {
                    coutner[num] = 0;
                }

                if (num_values_mode == MetadataMode::AVERAGE)
                    coutner[num] += 1;
                else if (num_values_mode == MetadataMode::MAX_AREA)
                    coutner[num] += model->get_area_in_border(border);
            }
            else if (it.value().is_string())
            {
                const string &str = it.value();
                if (metadata_.str.find(it.key()) == metadata_.str.end())
                {
                    metadata_.str[it.key()] = unordered_map<string, tfloat>();
                }

                auto &coutner = metadata_.str[it.key()];
                if (coutner.find(it.value()) == coutner.end())
                {
                    coutner[str] = 0;
                }

                coutner[str] += model->get_area_in_border(border);
            }
        }
    }

    consolidate_aggregated_metadata(metadata_, num_values_mode);
}

void QuadTreeLevel::consolidate_aggregated_metadata(const MetadataAggregate &metadata_, MetadataMode num_values_mode)
{
    for (auto it = metadata_.num.begin(); it != metadata_.num.end(); ++it)
    {
        const string &key = it->first;
        const auto &values = it->second;

        if (num_values_mode == MetadataMode::AVERAGE)
        {
            tfloat sum = 0;
            size_t count = 0;
            for (const auto & value : values)
            {
                sum += value.first * value.second;
                count += value.second;
            }
            metadata[key] = sum / count;
        }
        else if (num_values_mode == MetadataMode::MAX_AREA)
        {
            tfloat max_area = 0;
            tfloat max_value;
            for (const auto & value : values)
            {
                if (value.second > max_area)
                {
                    max_value = value.first;
                    max_area = value.second;
                }
            }
            metadata[key] = max_value;
        }
    }

    for (auto it = metadata_.str.begin(); it != metadata_.str.end(); ++it)
    {
        const string &key = it->first;
        const auto &values = it->second;
        
        size_t max_count = 0;
        string max_value;
        for (const auto & value : values)
        {
            if (value.second > max_count)
            {
                max_value = value.first;
                max_count = value.second;
            }
        }
        metadata[key] = max_value;
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
            if (border.inside(model->get_centroid()))
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

void QuadTreeLevel::filter_metadata(const vector<string> &keys)
{
    for (auto it = metadata.begin(); it != metadata.end();)
    {
        if (find(keys.begin(), keys.end(), it.key()) == keys.end())
        {
            it = metadata.erase(it);
        }
        else
        {
            ++it;
        }
    }

    if (ne != nullptr)
        ne->filter_metadata(keys);
    if (se != nullptr)
        se->filter_metadata(keys);
    if (sw != nullptr)
        sw->filter_metadata(keys);
    if (nw != nullptr)
        nw->filter_metadata(keys);
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
            if (border.inside(model->get_centroid()))
                model->to_gltf(gltf_model);
        }
    }

    tinygltf::TinyGLTF gltf;
    gltf.SetStoreOriginalJSONForExtrasAndExtensions(true);
    gltf.WriteGltfSceneToFile(&gltf_model, filename, true, true, true, true);
}