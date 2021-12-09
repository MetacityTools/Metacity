from typing import Tuple
from metacity.datamodel.project import Project
from metacity.core.grid.grid import Grid
from metacity.geometry import TriangularMesh
from metacity.utils.transform import tile_coords_in_range


def export_obj(project: Project, output_file: str, start: Tuple[float, float], end: Tuple[float, float]):
    written_verts = 0
    for layer in project.clayers(load_set=False):
        if layer.disabled:
            continue

        g = Grid(layer)
        tiles_coord = tile_coords_in_range(start, end, g.tile_size)
        for tile_coord in tiles_coord:
            print(tile_coord)
            tile = g[tile_coord]
            if tile is None:
                continue
            p: TriangularMesh = tile.polygon
            if p is None:
                continue
            m = p.slice_to_rect(start[0], start[1], end[0], end[1])
            if m is None:
                continue
            m.shift(-start[0], -start[1], 0)
            written_verts += m.to_obj(output_file, written_verts)

