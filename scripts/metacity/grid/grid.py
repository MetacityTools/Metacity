

from metacity.grid.config import RegularGridConfig


class RegularGrid:
    def __init__(self, dirtree):
        self.dirtree = dirtree


    @property
    def config(self):
        return RegularGridConfig(self.dirtree)

    

