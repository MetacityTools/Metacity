#include "legobuilder.hpp"
#include "bvh.hpp"
#include "png.hpp"

#include <iostream>
#include <fstream>

inline void validate_add(tfloat low, tfloat high, tfloat & factor, tfloat & out, tfloat & value) {
    if (value >= low && value <= high) {
        factor += 1.0f;
        out += value;
    }
}

void denoise(tfloat * height, unsigned int x, unsigned int y, tfloat low, tfloat high) {
    
    tfloat value;
    tfloat factor;
    bool t, b, r, l;
    for (size_t j = 0; j < y; j++)
    {
        for (size_t i = 0; i < x; i++)
        {
            if (height[j * x + i] < low || height[j * x + i] > high) {
                value = 0;
                factor = 0;

                t = (j == 0);
                b = (j == y - 1);
                r = (i == x - 1);
                l = (i == 0);
                
                //top row
                if (!t) {
                    if (!l)
                        validate_add(low, high, factor, value, height[(j - 1) * x + (i - 1)]);
                    validate_add(low, high, factor, value, height[(j - 1) * x + i]);
                    if (!r)
                        validate_add(low, high, factor, value, height[(j - 1) * (x + 1) + i]);
                }

                //mid row
                if (!l)
                    validate_add(low, high, factor, value, height[j * x + (i - 1)]);
                if (!r)
                    validate_add(low, high, factor, value, height[j * x + (i + 1)]);

                //bottom row
                if (!b) {
                    if (!l)
                        validate_add(low, high, factor, value, height[(j + 1) * x + (i - 1)]);
                    validate_add(low, high, factor, value, height[(j + 1) * x + i]);     
                    if (!r)
                        validate_add(low, high, factor, value, height[(j + 1) * x + (i + 1)]);
                }   

                height[j * x + i] = max(value / factor, low); 
            }
        }
    }
}

//===================================================================================================


LegoBuilder::LegoBuilder() {}

void LegoBuilder::insert_model(const shared_ptr<TriangularMesh> model)
{
    vertices.insert(vertices.end(), model->vertices.begin(), model->vertices.end());
}

//hopefully no one will trace anything higher then Mt. Everest
#define ORIGIN 10000

void LegoBuilder::build_heightmap(const tfloat xmin, const tfloat ymin, const tfloat xmax, const tfloat ymax, const size_t resolution_)
{
    BVH bvh(vertices);
    BBox box = bvh.bbox();
    
    //resolution per 1 unit of original coordinates
    resolution = resolution_;
    selected_box.min.x = xmin;
    selected_box.min.y = ymin;
    selected_box.min.z = box.min.z;
    selected_box.max.x = xmax;
    selected_box.max.y = ymax;
    selected_box.max.z = box.max.z;
    raster_dimx = (selected_box.max.x - selected_box.min.x) * resolution;
    raster_dimy = (selected_box.max.y - selected_box.min.y) * resolution;

    int ixmin = xmin * resolution;
    int iymin = ymin * resolution;
    tfloat unit_frag = 1.0 / resolution;  
 
    heightmap.clear();
    heightmap.reserve(raster_dimx * raster_dimy);

    for(int y = raster_dimy - 1; y >= 0; --y)
    {
        for(int x = 0; x < raster_dimx; ++x)
            heightmap.push_back(ORIGIN - bvh.traceDownRegualarRay((ixmin + x) * unit_frag, (iymin + y) * unit_frag, ORIGIN));
    }
    
    denoise(heightmap.data(), raster_dimx, raster_dimy, selected_box.min.z, selected_box.max.z);
}


tfloat min_func(vector<tfloat> & tile)
{
    tfloat mv = FLT_MAX;
    for(const auto & v : tile)
        mv = min(mv, v);
    return mv;
}

tfloat median_func(vector<tfloat> & tile)
{
    size_t n = tile.size() / 2;
    nth_element(tile.begin(), tile.begin()+n, tile.end());
    return tile[n];
}

//size of lego brick in milimeters
#define LEGODIM 8.0 //width
#define LEGOSTEP 3.2 //third of height

json LegoBuilder::legofy(const size_t box_size)
{
    lego_dimx = raster_dimx / box_size;
    lego_dimy = raster_dimy / box_size;

    //conver using tile funciton 
    vector<tfloat> tile;
    legomap.clear();
    legomap.reserve(lego_dimx * lego_dimy);
    for(size_t j = 0; j < lego_dimy; ++j)
        for(size_t i = 0; i < lego_dimx; ++i)
        {
            tile.clear();
            for (size_t y = j * box_size; y < min((j + 1) * box_size, raster_dimy); y++)
                for (size_t x = i * box_size; x < min((i + 1) * box_size, raster_dimx); x++)
                    tile.push_back(heightmap[x + y * raster_dimx]);
            legomap.push_back(median_func(tile));
        }

    //found bounds in z axis
    tfloat lego_height_min = FLT_MAX, lego_height_max = FLT_MIN;
    for(const auto & t: legomap)
        lego_height_min = min(t, lego_height_min), lego_height_max = max(t, lego_height_max);
    selected_box.min.z = lego_height_min;
    selected_box.max.z = lego_height_max;
    
    //compute dims
    tfloat unit_per_lego_brick = (tfloat) box_size / (tfloat) resolution;
    tfloat unit_per_real_mm = (unit_per_lego_brick / LEGODIM);
    tfloat height_step_resolution = unit_per_real_mm * LEGOSTEP;
    tfloat height_range = lego_height_max - lego_height_min;
    lego_dimz = height_range / height_step_resolution;

    //sample according to real dimensions
    for(auto & t: legomap)
        t = floor((t - lego_height_min) / height_step_resolution);


    //produce height map (number of bricks)
    vector<vector<uint8_t>> lego_heightmap;
    lego_heightmap.reserve(lego_dimy);    
    for (size_t y = 0; y < lego_dimy; y++)
    {
        vector<uint8_t> line;
        for (size_t x = 0; x < lego_dimx; x++)  
            line.push_back((legomap[x + y * lego_dimx]));
        lego_heightmap.emplace_back(move(line));
    }


    return {
        {"coord_size", {
            {"x", selected_box.max.x - selected_box.min.x},
            {"y", selected_box.max.y - selected_box.min.y},
            {"z", selected_box.max.z - selected_box.min.z}
        }},
        {"model_size_mm", {
            {"x", lego_dimx * LEGODIM},
            {"y", lego_dimy * LEGODIM},
            {"z", lego_dimz * LEGOSTEP}
        }},
        {"lego_size", {
            {"x", lego_dimx},
            {"y", lego_dimy},
            {"z", lego_dimz}
        }},
        {"map", lego_heightmap}
    };
}

void LegoBuilder::lego_to_png(const string & name) const
{
    vector<uint8_t> image;
    image.reserve(lego_dimx * lego_dimy * 3);
    uint8_t byte;
    for(const auto & b: legomap)
    {
        byte = (b / lego_dimz * 255);
        image.push_back(byte);
        image.push_back(byte);
        image.push_back(byte);
    }

    std::ofstream out(name, std::ios::binary);
    TinyPngOut pngout(static_cast<uint32_t>(lego_dimx), static_cast<uint32_t>(lego_dimy), out);
    pngout.write(image.data(), static_cast<size_t>(lego_dimx * lego_dimy));
}

