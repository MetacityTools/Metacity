#include "layer.hpp"
#include "gltf/tiny_gltf.h"
#include "progress.hpp"

Layer::Layer() {}

void Layer::add_model(shared_ptr<Model> model) {
    models.push_back(model);
}

void Layer::add_models(const vector<shared_ptr<Model>> & models) {
    this->models.insert(this->models.end(), models.begin(), models.end());
}

vector<shared_ptr<Model>> Layer::get_models() const {
    return models;
}

void Layer::to_gltf(const string &filename) const {
    tinygltf::Model gltf_model;
    tinygltf::Asset asset;
    asset.version = "2.0";
    asset.generator = "Metacity";
    gltf_model.asset = asset;
    
    Progress bar("Exporting models");
    for (auto model : models) {
        bar.update();
        model->to_gltf(gltf_model);
    }

    tinygltf::TinyGLTF gltf;
    //gltf.SetStoreOriginalJSONForExtrasAndExtensions(true);
    gltf.WriteGltfSceneToFile(&gltf_model, filename, true, true, true, false);
}

void Layer::from_gltf(const string &filename) {
    tinygltf::TinyGLTF gltf;
    //gltf.SetStoreOriginalJSONForExtrasAndExtensions(true);
    tinygltf::Model gltf_model;
    string err, warn;

    Progress bar("Importing models");
    bool ret = gltf.LoadASCIIFromFile(&gltf_model, &err, &warn, filename);

    if (!err.empty()) {
        cout << err << endl;
    }

    if (!warn.empty()) {
        cout << warn << endl;
    }

    if (!ret) {
        cout << "Failed to load gltf file" << endl;
        return;
    }

    for (int mesh_idx = 0; mesh_idx < gltf_model.meshes.size(); mesh_idx++) {
        bar.update();
        auto model = make_shared<Model>();
        model->from_gltf(gltf_model, mesh_idx);
        add_model(model);
    } 
}