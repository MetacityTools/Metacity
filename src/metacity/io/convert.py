from metacity.utils.filesystem import read_json, filename, change_suffix, concat
import metacity.io.pyshp.pyshp as shapefile
from metacity.io.geobuf import encode



def shp_to_pbf(shp_file: str, buff_dir: str):
    """
    Convert a SHP file to a PBF file.
    """

    shapefile.VERBOSE = False
    sf = shapefile.Reader(shp_file)
    geo = sf.shapeRecords().__geo_interface__
    buff_file = change_suffix(filename(shp_file), "pbf")
    buff_file = concat(buff_dir, buff_file)
    with open(buff_file, 'wb') as f:
        f.write(encode(geo))



