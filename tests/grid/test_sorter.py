from numpy.core.fromnumeric import sort
from metacity.utils.sorter import GridSorter
import numpy as np


def test_sorter():
    x_planes = [1.0, 2.0]
    y_planes = [1.5]
    points = np.array([[0, 0, 0], 
              [1, 1, 1], 
              [5, 5, 5], 
              [4, 4, 4], 
              [0.5, 1.5, 0.5], 
              [1.0, 0.5, 0],
              [1.0, 1.5, 0.0],
              [2.0, 1.5, 0.0]])

    expected = {
        (0, 0): np.array([[0, 0, 0], [1, 1, 1], [0.5, 1.5, 0.5], [1.0, 0.5, 0], [1.0, 1.5, 0.0]]),
        (2, 1): np.array([[5, 5, 5], [4, 4, 4]]),
        (1, 0): np.array([[2.0, 1.5, 0.0]])
    }

    sorter = GridSorter(x_planes, y_planes)
    for point in points:
        sorter.insert(point, point)

    assert sorter.partitions.keys() == expected.keys()
    for idx in expected.keys():
        assert np.all(expected[idx] == np.array(sorter.partitions[idx]))

