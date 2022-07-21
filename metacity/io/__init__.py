from metacity.io.geojson import parse as parse_geojson
from metacity.io.shapefile import parse as parse_shapefile
import metacity.utils.filesystem as fs
from metacity.geometry import Progress 

__all__ = ["parse", "parse_recursively"]

def parse(file: str, progress: Progress = None):
    if file.endswith('.shp'):
        return parse_shapefile(file, progress)
    elif file.endswith('.json'):
        return parse_geojson(file, progress)


def parse_recursively(directory: str):
    models = []
    progress = Progress("Loading Models")
    for file in fs.list_files_recursive(directory):
        data = parse(file, progress)
        if data is not None:
            models.extend(parse(file))
    return models

