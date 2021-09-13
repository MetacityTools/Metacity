import numpy as np
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.grid.build import build_grid
from metacity.io.cityjson.parser import parse
from metacity.filesystem import grid as fs

import subprocess


def test_build_cache(layer: MetacityLayer, railway_dataset, railway_dataset_stats):
    stats = railway_dataset_stats
    parse(layer, railway_dataset)
    grid = build_grid(layer, 1000)

    #dir = fs.grid_cache_dir(grid.dir)
    #result = subprocess.run(["tree", dir], stderr=subprocess.PIPE, text=True)
    #print(result.stderr)
    