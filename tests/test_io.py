from metacity.io.parse import parse


def test_geojson(geojson_dataset: str):
    objects = parse(geojson_dataset)
    assert len(objects) == 14

def test_shp_line(shp_line_dataset: str):
    objects = parse(shp_line_dataset)
    assert len(objects) == 5041

def test_shp_poly(shp_poly_dataset: str):
    objects = parse(shp_poly_dataset)
    assert len(objects) == 2826


    


