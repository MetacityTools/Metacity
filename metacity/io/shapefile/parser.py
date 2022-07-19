import fiona
import geopandas
from metacity.utils import filesystem as fs
from metacity.io.geojson.parser import parse_data as parse_geojson


def parse(shp_file: str):
    """
    Parse a SHP file. All contents are transformed into Metacity objects, and returned as a list.

    Args:
        shp_file (str): Path to the SHP file.
    
    Returns:
        list: List of Metacity objects.

    See Also:
            :func:`metacity.io.parse' to see other formats.

    """
    file = geopandas.read_file(shp_file)
    #gjson_file = fs.change_suffix(shp_file, 'json')
    data = file._to_geo()
    #file.to_file(gjson_file, driver='GeoJSON')
    return parse_geojson(data)

