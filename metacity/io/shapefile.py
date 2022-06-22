import fiona
import geopandas
from metacity.utils import filesystem as fs
from metacity.io.geojson import parse_data as parse_geojson

__all__ = ["parse"]


def parse(shp_file: str):
    file = geopandas.read_file(shp_file)
    data = file._to_geo()
    return parse_geojson(data)

