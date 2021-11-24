#include "polygons.hpp"


class LegoBuilder {
public:
    LegoBuilder();
    void insert_model(const shared_ptr<TriangularMesh> model);
    void build_heightmap(const tfloat xmin, const tfloat ymin, const tfloat xmax, const tfloat ymax, const uint32_t xresolution);
    json legofy(const int box_size);
    void lego_to_png(const string & name) const;

protected:
    vector<tvec3> vertices;
    vector<tfloat> heightmap;
    vector<tfloat> legomap;

    int ixmin = 0;
    int ixmax = 0;
    int iymin = 0;
    int iymax = 0;
    uint32_t resolution = 0;

    size_t xdim = 0;
    size_t ydim = 0;
    size_t lego_dimx = 0;
    size_t lego_dimy = 0;
    tfloat hmin = 0;
    tfloat hmax = 0;
};


