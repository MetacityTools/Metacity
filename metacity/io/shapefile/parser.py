from metacity.datamodel.layer.layer import MetacityLayer
import geopandas
from metacity.filesystem import file as fs
from metacity.io.geojson.parser import parse as parse_json


def parse(layer: MetacityLayer, shp_file: str):
    file = geopandas.read_file(shp_file)
    gjson_file = fs.change_suffix(shp_file, 'json')
    file.to_file(gjson_file, driver='GeoJSON')
    parse_json(layer, gjson_file)

