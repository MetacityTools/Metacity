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

//resolution is a resolution per 1 unit of dimensions
void LegoBuilder::build_heightmap(const tfloat xmin, const tfloat ymin, const tfloat xmax, const tfloat ymax, const uint32_t resolution_)
{
    BVH bvh(vertices);

    BBox box = bvh.bbox();
    hmin = box.min.z;
    hmax = box.max.z;

    ixmin = xmin * resolution_;
    ixmax = xmax * resolution_;
    iymin = ymin * resolution_;
    iymax = ymax * resolution_;

    tfloat unit_frag = 1.0 / resolution_;  

    xdim = (xmax - xmin) * resolution_;
    ydim = (ymax - ymin) * resolution_;
    
    heightmap.clear();
    heightmap.reserve(xdim * ydim);



    for(int y = ydim - 1; y >= 0; --y)
    {
        for(int x = 0; x < xdim; ++x)
            heightmap.push_back(ORIGIN - bvh.traceDownRegualarRay((ixmin + x) * unit_frag, (iymin + y) * unit_frag, ORIGIN));
    }
    
    denoise(heightmap.data(), xdim, ydim, hmin, hmax);
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

#define LEGODIM 8

json LegoBuilder::legofy(const int box_size)
{
    lego_dimx = xdim / box_size;
    lego_dimy = ydim / box_size;

    vector<tfloat> tile;
    legomap.clear();
    legomap.reserve(lego_dimx * lego_dimy);

    for(size_t j = 0; j < lego_dimy; ++j)
        for(size_t i = 0; i < lego_dimx; ++i)
        {
            tile.clear();
            for (size_t y = j * box_size; y < min((j + 1) * box_size, ydim); y++)
                for (size_t x = i * box_size; x < min((i + 1) * box_size, xdim); x++)
                    tile.push_back(heightmap[x + y * xdim]);

            legomap.push_back(median_func(tile));
        }

    tfloat vmin = FLT_MAX, vmax = FLT_MIN;
    uint8_t byte; 
    for(const auto & t: legomap)
        vmin = min(t, vmin), vmax = max(t, vmax);
    tfloat range = vmax - vmin;

    //tfloat scale = 
    //size_t z_dim = 


    return {
        {"real size", {
            {"x", lego_dimx * LEGODIM},
            {"y", lego_dimy * LEGODIM},
            {"z"}
        }},
        {"dims", {
            {"x", lego_dimx},
            {"y", lego_dimy},
            
        }}
    };
}

void LegoBuilder::lego_to_png(const string & name) const
{
    tfloat vmin = FLT_MAX, vmax = FLT_MIN;
    uint8_t byte; 
    for(const auto & t: legomap)
        vmin = min(t, vmin), vmax = max(t, vmax);
    tfloat range = vmax - vmin;

    vector<uint8_t> image;
    image.reserve(lego_dimx * lego_dimy * 3);
    for(const auto & h: legomap)
    {
        byte = (h - vmin) / range * 255;
        image.push_back(byte);
        image.push_back(byte);
        image.push_back(byte);
    }

    std::ofstream out(name, std::ios::binary);
    TinyPngOut pngout(static_cast<uint32_t>(lego_dimx), static_cast<uint32_t>(lego_dimy), out);
    pngout.write(image.data(), static_cast<size_t>(lego_dimx * lego_dimy));
}

