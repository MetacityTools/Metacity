from metacity.grid import build


def test_generate_layout(grid, random_bbox):
    build.generate_layout(grid, random_bbox, 20)

