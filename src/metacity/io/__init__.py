from metacity.io.geojson import parse as parse_geojson
from metacity.io.shapefile import parse as parse_shapefile
from metacity.io.obj import parse as parse_obj

import metacity.utils.filesystem as fs
from metacity.geometry import Progress 

__all__ = ["parse", "parse_recursively"]


def parse(file: str, progress: Progress = None):
    if progress is None:
        progress = Progress("Loading Model")

    if file.endswith('.shp'):
        return parse_shapefile(file, progress)
    elif file.endswith('.json'):
        return parse_geojson(file, progress)
    elif file.endswith('.obj'):
        return parse_obj(file, progress)



def parse_recursively(directory: str):
    models = []
    progress = Progress("Loading Models")
    for file in fs.list_files_recursive(directory):
        submodels = parse(file, progress)
        if submodels is not None:
            models.extend(submodels)
    return models

        