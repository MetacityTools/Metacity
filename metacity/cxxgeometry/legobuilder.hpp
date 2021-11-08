#include "polygons.hpp"


class LegoBuilder {
public:
    LegoBuilder();
    void insert_model(const shared_ptr<SimpleMultiPolygon> model);
    void build_heightmap(const tfloat xmin, const tfloat ymin, const tfloat xmax, const tfloat ymax, const uint32_t xresolution);
    void legofy(const int box_size);
    void lego_to_png(const string & name) const;

protected:
    vector<tvec3> vertices;
    vector<tfloat> heightmap;
    vector<tfloat> legomap;
    size_t xdim = 0;
    size_t ydim = 0;
    size_t lego_dimx = 0;
    size_t lego_dimy = 0;
    tfloat hmin = 0;
    tfloat hmax = 0;
};


