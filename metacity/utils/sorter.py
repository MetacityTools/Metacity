import bisect
from typing import List


class GridSorter:
    def __init__(self, x_planes: List[int], y_planes: List[int]):
        self.x_planes = x_planes
        self.x_planes.sort()
        self.y_planes = y_planes
        self.y_planes.sort()
        self.partitions = {}

    def get_point_idx(self, point):
        x = bisect.bisect_left(self.x_planes, point[0])
        y = bisect.bisect_left(self.y_planes, point[1])
        return x, y

    def insert(self, element, point):
        idx = self.get_point_idx(point)
        if idx not in self.partitions:
            self.partitions[idx] = []
        self.partitions[idx].append(element)
        

