#pragma once
#include "bvh.hpp"
#include "model.hpp"


namespace modifiers {
    shared_ptr<Model> simplify_envelope(shared_ptr<Model> model);
    shared_ptr<Model> merge_models(const vector<shared_ptr<Model>> & models);
    void simplify_remesh_height(vector<shared_ptr<Model>> & models, const tfloat tile_side, const size_t tile_divisions);
    void map_to_height(BVH & bvh, vector<shared_ptr<Model>> & models);
    void move_to_plane_z(vector<shared_ptr<Model>> & models, const tfloat plane);
}