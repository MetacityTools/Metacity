from metacity.datamodel.grid.grid import RegularGrid
from metacity.grid import build
import numpy as np

def test_slicing_planes(grid: RegularGrid, random_bbox):
    build.generate_layout(grid, random_bbox, 20)
    x_planes, y_planes = grid.splitting_planes()
    xp, yp = np.array(x_planes), np.array(y_planes)
    dx, dy = np.diff(xp), np.diff(yp)
    ts = grid.config.tile_size
    res = grid.config.resolution

    assert ts > 0
    assert len(xp) == res[0]
    assert len(yp) == res[1]
    assert np.all(dx == ts) 
    assert np.all(dy == ts)
