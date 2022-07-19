from metacity.io.geojson import parse as parse_geojson
from metacity.io.shapefile import parse as parse_shapefile
import metacity.utils.filesystem as fs
from tqdm import tqdm

__all__ = ["parse", "parse_recursively"]

def parse(file: str):
    if file.endswith('.shp'):
        return parse_shapefile(file)
    elif file.endswith('.json'):
        return parse_geojson(file)


def parse_recursively(directory: str):
    models = []
    for file in tqdm(fs.list_files_recursive(directory)):
        data = parse(file)
        if data is not None:
            models.extend(parse(file))
    return models

