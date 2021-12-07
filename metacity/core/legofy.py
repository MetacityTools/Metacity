from typing import Tuple
from metacity.datamodel.project import Project
from metacity.geometry import LegoBuilder
from metacity.core.grid.grid import Grid
from metacity.filesystem.base import write_json
import metacity.filesystem.base as fs
from tqdm import tqdm
from metacity.utils.transform import tile_coords_in_range
import os


def legofy(project: Project, output_dir: str, start: Tuple[float, float], end: Tuple[float, float], coordinates_decimal_precision=2, box_filter_size_range=(5, 45), box_filter_step=5):
    """
    Generate lego tiles from a project. The lego tiles are generated in the output directory, stores json and png with heightmap.
    
    Args:
        project (str): The project to generate lego tiles from.
        output_dir (str): The directory to write the lego tiles to.
        start (Tuple[float, float]): The start coordinates of the lego tiles.
        end (Tuple[float, float]): The end coordinates of the lego tiles.
        coordinates_decimal_precision (int): The number of decimal places to round the coordinates to.
        box_filter_size_range (Tuple[int, int]): The range of box filter sizes to use.
        box_filter_step (int): The step size of the box filter.

    Returns:
        None
    """

    fs.create_dir_if_not_exists(output_dir)
    tiles = tile_coords_in_range(start, end, 1000)
    builder = LegoBuilder()

    for xy in tqdm(tiles):
        for layer in project.layers:
            if layer.disabled:
                continue
            grid = Grid(layer)
            tile = grid[xy]
            if tile is None:
                continue
            polygon = tile.polygon
            if polygon is None:
                continue
            builder.insert_model(polygon)

    builder.build_heightmap(start[0], start[1], end[0], end[1], coordinates_decimal_precision)

    for i in tqdm(range(box_filter_size_range[0], box_filter_size_range[1], box_filter_step)):
        config = builder.legofy(i)
        write_json(os.path.join(output_dir, f"lego{i}.json"), config)
        builder.lego_to_png(os.path.join(output_dir, f"layout{i}.png"))
