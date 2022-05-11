from metacity.filesystem import base as fs
#from metacity.io.cityjson.parser import parse as parse_cj
from metacity.io.geojson.parser import parse as parse_gj
from metacity.io.shapefile.parser import parse as parse_shp
import os

def parse_json(input_file: str):
    """
    Parse a GeoJSON file. All contents are transformed into Metacity objects, and returned as a list.

    Args:
        input_file (str): Path to the GeoJSON file.

    Returns:
        list: List of Metacity objects.
    """
    try:
        return parse_gj(input_file)
    except Exception as e:
        e2 = str(e)
    raise Exception(f"Could not parse {input_file}: \nGeoJSON parser:{e2}")


def parse_shapefile(input_file: str):
    """
    Parse a Shapefile. All contents are transformed into Metacity objects, and returned as a list.

    Args:
        input_file (str): Path to the Shapefile.
    
    Returns:
        list: List of Metacity objects.
    """
    try:
        return parse_shp(input_file)
    except Exception as e:
        raise Exception(f"Could not parse {input_file}: \nSHP parser:{e}")


def parse(input_file: str):
    """
    Parse a file. All contents are transformed into Metacity objects, and returned as a list.
    
    Args:
        input_file (str): Path to the file.

    Returns:
        list: List of Metacity objects or None if the file could not be parsed.
    """
    suffix = fs.get_suffix(input_file)
    if suffix == 'json':
        return parse_json(input_file)
    elif suffix == 'shp':
        return parse_shapefile(input_file)


def parse_tree(input_dir: str):
    """
    Generator, parses a contents of a directory recursively. All contents are transformed 
    into Metacity objects, and returned as a list. Yields Metacity objects one by one.

    Args:
        input_dir (str): Path to the directory.
    """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            data = parse(file_path)
            if data is not None:
                for o in data:
                    yield o



