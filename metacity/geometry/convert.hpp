#pragma once
#include "gltf/json.hpp"
#include "gltf/tiny_gltf.h"

using namespace std;

//nlohmann::json to tinygltf::Value
static tinygltf::Value to_gltf_value(const nlohmann::json & data)
{
    if (data.is_array()) {
        std::vector<tinygltf::Value> array;
        for (auto & item : data) {
            if (item.is_array()) {
                array.push_back(to_gltf_value(item));
            } else if (item.is_object()) {
                array.push_back(to_gltf_value(item));
            } else if (item.is_number_integer()) {
                array.push_back(tinygltf::Value(item.get<int>()));
            } else if (item.is_number_float()) {
                array.push_back(tinygltf::Value(item.get<float>()));
            } else if (item.is_string()) {
                array.push_back(tinygltf::Value(item.get<string>()));
            } else if (item.is_boolean()) {
                array.push_back(tinygltf::Value(item.get<bool>()));
            } else {
                throw runtime_error("Unsupported type");
            }
        }
        return tinygltf::Value(array);
    }

    if (data.is_object()) {
        std::map<std::string, tinygltf::Value> value;
        for (auto & pair : data.items()) {
            if (pair.value().is_number_integer()) {
                value[pair.key()] = tinygltf::Value(pair.value().get<int>());
            } else if (pair.value().is_number_float()) {
                value[pair.key()] = tinygltf::Value(pair.value().get<double>());
            } else if (pair.value().is_string()) {
                value[pair.key()] = tinygltf::Value(pair.value().get<string>());
            } else if (pair.value().is_boolean()) {
                value[pair.key()] = tinygltf::Value(pair.value().get<bool>());
            } else if (pair.value().is_array()) {
                value[pair.key()] = to_gltf_value(pair.value());
            } else if (pair.value().is_object()) {
                value[pair.key()] = to_gltf_value(pair.value());
            }
        }
        return tinygltf::Value(value);
    }

    return tinygltf::Value();
};

//tinygltf::Value to nlohmann::json
static nlohmann::json to_json_value(const tinygltf::Value & value)
{
    if (value.IsArray()) {
        nlohmann::json array;
        for (size_t i = 0; i < value.Size(); i++) {
            const auto & item = value.Get(i);
            if (item.IsArray()) {
                array.push_back(to_json_value(item));
            } else if (item.IsObject()) {
                array.push_back(to_json_value(item));
            } else if (item.IsInt()) {
                array.push_back(item.Get<int>());
            } else if (item.IsReal()) {
                array.push_back(item.Get<double>());
            } else if (item.IsString()) {
                array.push_back(item.Get<string>());
            } else if (item.IsBool()) {
                array.push_back(item.Get<bool>());
            } else {
                throw runtime_error("Unsupported type");
            }
        }
        return array;
    }

    if (value.IsObject()) {
        nlohmann::json object;
        for (const auto & key : value.Keys()) {
            const auto & item = value.Get(key);
            if (item.IsArray()) {
                object[key] = to_json_value(item);
            } else if (item.IsObject()) {
                object[key] = to_json_value(item);
            } else if (item.IsInt()) {
                object[key] = item.Get<int>();
            } else if (item.IsReal()) {
                object[key] = item.Get<double>();
            } else if (item.IsString()) {
                object[key] = item.Get<string>();
            } else if (item.IsBool()) {
                object[key] = item.Get<bool>();
            } else {
                throw runtime_error("Unsupported type");
            }
        }
        return object;
    }

    return nlohmann::json();
};