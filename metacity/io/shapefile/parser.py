import fiona
import geopandas
from metacity.filesystem import base as fs
from metacity.io.geojson.parser import parse_data as parse_geojson


def parse(shp_file: str):
    file = geopandas.read_file(shp_file)
    #gjson_file = fs.change_suffix(shp_file, 'json')
    data = file._to_geo()
    #file.to_file(gjson_file, driver='GeoJSON')
    return parse_geojson(data)

