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
    onplane = (triangle[:, axis] == plane)
    
    if np.count_nonzero(onplane) != 1:
        raise Exception(f"No or multiple points on plane: {onplane}.")
    
    a_onplane, b_onplane, c_onplane = onplane

    if a_onplane:
        return one_on_plane_split(a, b, c, plane, axis)

    if b_onplane:
        return one_on_plane_split(b, c, a, plane, axis)

    if c_onplane:
        return one_on_plane_split(c, a, b, plane, axis)


def roll_triangle(triangle, plane, axis):
    positioned = False
    while not positioned:
        leftplane = triangle[:, axis] < plane
        positioned = (leftplane[1] and leftplane[2]) or not (leftplane[1] or leftplane[2])
        if not positioned:
            triangle = np.roll(triangle, 1, axis=0)
    
    return triangle


def general_triangle_split(triangle, plane, axis):
    triangle = roll_triangle(triangle, plane, axis)
    a, b, c = triangle
    mid_ab = cross_point(a, b, plane, axis)
    mid_ac = cross_point(a, c, plane, axis)
    dist_ab_c = np.sum((mid_ab - c) ** 2)
    dist_b_ac = np.sum((b - mid_ac) ** 2)

    if dist_ab_c > dist_b_ac:
        return [ np.array([ a, mid_ab, mid_ac ]), np.array([ mid_ab, b, mid_ac ]), np.array([ b, c, mid_ac ]) ]
    else:
        return [ np.array([ a, mid_ab, mid_ac ]), np.array([ mid_ab, b, c ]), np.array([ mid_ab, c, mid_ac ]) ]


def element_not_splitable(triangle, plane, axis):
    return np.all(triangle[:, axis] <= plane) or np.all(triangle[:, axis] >= plane)


def point_on_plane(triangle, plane, axis):
    return np.any(triangle[:, axis] == plane)


def split_triangle_along_axis(triangle, plane, axis):
    if element_not_splitable(triangle, plane, axis):
        return [ triangle ]

    if point_on_plane(triangle, plane, axis):
        return special_case_split(triangle, plane, axis)
    else:
        return general_triangle_split(triangle, plane, axis)


def general_line_split(line, plane, axis):
    a, b = line
    a, b = (a, b) if a[axis] < b[axis] else (b, a)
    mid_ab = cross_point(a, b, plane, axis)
    return [ np.array([a, mid_ab]), np.array([mid_ab, b]) ]


def split_line_along_axis(line, plane, axis):
    if element_not_splitable(line, plane, axis):
        return [ line ]
    return general_line_split(line, plane, axis)


def split_triangles_along_axis(triangles, planes, axis):
    for plane in planes:
        tri_split = []
        for tri in triangles:
            tri_split.extend(split_triangle_along_axis(tri, plane, axis))

        triangles = tri_split
    return np.array(triangles)


def split_lines_along_axis(lines, planes, axis):
    for plane in planes:
        line_split = []
        for lin in lines:
            line_split.extend(split_line_along_axis(lin, plane, axis))

        lines = line_split
    return np.array(lines)


def split_triangle(triangle, x_planes, y_planes):
    triangles = split_triangles_along_axis([triangle], x_planes, 0)
    triangles = split_triangles_along_axis(triangles, y_planes, 1)
    return triangles


def split_line(line, x_planes, y_planes):
    lines = split_lines_along_axis([line], x_planes, 0)
    lines = split_lines_along_axis(lines, y_planes, 1)
    return lines