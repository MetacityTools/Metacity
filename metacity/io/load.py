from json import loads
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.filesystem import file as fs
from metacity.io.cityjson.parser import parse as parse_cj
from metacity.io.geojson.parser import parse as parse_gj
from metacity.io.shapefile.parser import parse as parse_shp
from typing import List


def parse_json(layer: MetacityLayer, input_file: str):
    try:
        parse_cj(layer, input_file)
        return 
    except Exception as e:
        e1 = str(e)
    try:
        parse_gj(layer, input_file)
        return
    except Exception as e:
        e2 = str(e)
    raise Exception(f"Could not parse {input_file}: \nCityJSON parser:{e1}\nGeoJSON parser:{e2}")


def parse_shp(layer: MetacityLayer, input_file: str):
    try:
        parse_shp(layer, input_file)
    except Exception as e:
        raise Exception(f"Could not parse {input_file}: \nSHP parser:{e}")


def load(layer: MetacityLayer, input_file: str):
    suffix = fs.get_suffix(input_file)
    if suffix == 'json':
        parse_json(layer, input_file)
    elif suffix == 'shp':
        parse_shp(layer, input_file)
    else:
        raise Exception(f"Could not parse {input_file}: unknown suffix")
