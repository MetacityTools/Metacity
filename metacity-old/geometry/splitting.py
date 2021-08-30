import numpy as np


def cross_point(a, b, plane, axis):
    p = (plane - b[axis]) / (a[axis] - b[axis])
    return a * p + b * (1 - p)


def one_on_plane_split(x_on_plane, y, z, plane, axis):
    mid = cross_point(y, z, plane, axis)
    y_triangle = np.array([y, mid, x_on_plane])
    z_triangle = np.array([x_on_plane, mid, z])
    return [ y_triangle, z_triangle ]


def special_case_split(triangle, plane, axis):
    a, b, c = triangle
    onplane = (triangle[:, 0] == plane)
    
    if np.count_nonzero(onplane) != 1:
        raise Exception(f"No or multiple points on plane: {onplane}.")
    
    a_onplane, b_onplane, c_onplane = onplane

    if a_onplane:
        return one_on_plane_split(a, b, c, plane, axis)

    if b_onplane:
        return one_on_plane_split(b, c, a, plane, axis)

    if c_onplane:
        return one_on_plane_split(c, a, b, plane, axis)


def roll(triangle, plane, axis):
    positioned = False
    while not positioned:
        leftplane = triangle[:, axis] < plane
        positioned = (leftplane[1] and leftplane[2]) or not (leftplane[1] or leftplane[2])
        if not positioned:
            triangle = np.roll(triangle, 1, axis=0)
    
    return triangle



def general_split(triangle, plane, axis):
    triangle = roll(triangle, plane, axis)
    a, b, c = triangle
    mid_ab = cross_point(a, b, plane, axis)
    mid_ac = cross_point(a, c, plane, axis)
    dist_ab_c = np.sum((mid_ab - c) ** 2)
    dist_b_ac = np.sum((b - mid_ac) ** 2)

    if dist_ab_c > dist_b_ac:
        return [ np.array([ a, mid_ab, mid_ac ]), np.array([ mid_ab, b, mid_ac ]), np.array([ b, c, mid_ac ]) ]
    else:
        return [ np.array([ a, mid_ab, mid_ac ]), np.array([ mid_ab, b, c ]), np.array([ mid_ab, c, mid_ac ]) ]


def triangle_not_splitable(triangle, plane, axis):
    return np.all(triangle[:, axis] <= plane) or np.all(triangle[:, axis] >= plane)


def point_on_plane(triangle, plane, axis):
    return np.any(triangle[:, axis] == plane)


def split(triangle, plane, axis):
    if triangle_not_splitable(triangle, plane, axis):
        return [ triangle ]

    if point_on_plane(triangle, plane, axis):
        return special_case_split(triangle, plane, axis)
    else:
        return general_split(triangle, plane, axis)


def split_along_planes(triangles, planes, axis):
    tri_split = []
    for plane in planes:
        for tri in triangles:
            tri_split.extend(split(tri, plane, axis))

        triangles = tri_split
        tri_split = []
    return np.array(triangles)
