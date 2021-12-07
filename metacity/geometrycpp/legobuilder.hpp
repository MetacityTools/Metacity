#include "polygons.hpp"
#include "bbox.hpp"

class LegoBuilder {
public:
    LegoBuilder();
    void insert_model(const shared_ptr<TriangularMesh> model);
    void build_heightmap(const tfloat xmin, const tfloat ymin, const tfloat xmax, const tfloat ymax, const size_t xresolution);
    json legofy(const size_t box_size);
    void lego_to_png(const string & name) const;

protected:
    vector<tvec3> vertices;
    vector<tfloat> heightmap;
    vector<tfloat> legomap;

    //original rectangle border coordinates multiplied by resolution
    BBox selected_box;
    //resolution of original unit (precision)
    size_t resolution = 0;
    //dimensions in units times resolution
    size_t raster_dimx = 0;
    size_t raster_dimy = 0;
    //lego dimensions
    size_t lego_dimx = 0;
    size_t lego_dimy = 0;
    size_t lego_dimz = 0;
};


