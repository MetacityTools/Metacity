from metacity.filesystem import grid as fs


class RegularGrid:
    def __init__(self, layer_dir):
        self.dir = fs.grid_dir(layer_dir)
