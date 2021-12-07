from typing import Tuple


def tile_coords_in_range(start: Tuple[float, float], end: Tuple[float, float], tile_size: int):
    xrange = (int(start[0] // tile_size), int(end[0] // tile_size) + 1)
    yrange = (int(start[1] // tile_size), int(end[1] // tile_size) + 1)
    return [ (x, y) for x in range(*xrange) for y in range(*yrange) ]
