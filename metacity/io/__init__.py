from metacity.io.geojson import parse as parse_geojson
from metacity.io.shapefile import parse as parse_shapefile
from metacity.io.osm_graph import parse_graph as parse_osm_graph
import metacity.utils.filesystem as fs
from metacity.geometry import Progress 

__all__ = ["parse", "parse_recursively"]


def parse(file: str, from_crs: str = None, to_crs: str = None, progress: Progress = None):
    if progress is None:
        progress = Progress("Loading Model")

    if file.endswith('.shp'):
        return parse_shapefile(file, from_crs, to_crs, progress)
    elif file.endswith('.json'):
        return parse_geojson(file, from_crs, to_crs, progress)


def parse_graph(node_file: str, edge_file: str, from_crs: str = None, to_crs: str = None):
    return parse_osm_graph(node_file, edge_file, from_crs, to_crs)


def parse_recursively(directory: str, from_crs: str = None, to_crs: str = None):
    models = []
    progress = Progress("Loading Models")
    for file in fs.list_files_recursive(directory):
        submodels = parse(file, from_crs, to_crs, progress)
        if submodels is not None:
            models.extend(submodels)
    return models

