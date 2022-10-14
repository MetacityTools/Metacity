import metacity.io.pyshp.pyshp as shapefile
from metacity.io.geojson import parse_data as parse_geojson
from metacity.geometry import Progress

__all__ = ["parse"]


def parse(shp_file: str, progress: Progress = None):
    """
    Parse a SHP file. All contents are transformed into Metacity objects, and returned as a list.

    Args:
        shp_file (str): Path to the SHP file.
        from_crs (str): Optional. The CRS of the input file.
        to_crs (str): Optional. The CRS to transform the input file to.
    
    Returns:
        list: List of Metacity objects.

    See Also:
            :func:`metacity.io.parse' to see other formats.

    """
    shapefile.VERBOSE = False
    sf = shapefile.Reader(shp_file)
    geo = sf.shapeRecords().__geo_interface__
    return parse_geojson(geo, progress)


