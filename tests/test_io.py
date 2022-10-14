from metacity.io.geojson import parse as parse_geojson
from metacity.io.shapefile import parse as parse_shp
from metacity.io import parse_recursively
from metacity.io.convert import shp_to_pbf

def test_geojson(geojson_dataset: str):
    objects = parse_geojson(geojson_dataset)
    assert len(objects) == 24


def test_shp_line(shp_line_dataset: str):
    objects = parse_shp(shp_line_dataset)
    assert len(objects) == 5041


def test_shp_poly(shp_poly_dataset: str):
    objects = parse_shp(shp_poly_dataset)
    assert len(objects) == 2826


def test_recursive_parse(geometry_directory):
    objects = [ o for o in parse_recursively(geometry_directory) ]
    assert len(objects) == 2826 + 5041 + 24
    

def test_convert(shp_poly_dataset: str, tmp_directory: str):
    shp_to_pbf(shp_poly_dataset, tmp_directory)
    
