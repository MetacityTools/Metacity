import metacity.geometry.primitive as p
import metacity.utils.encoding as e
from pprint import pprint as print


points = p.MultiPoint()
data = [5, 6, 4, 8, 4, 6]
points.push_p2(data)
print(points.contents())
points.push_p3(data)
print(points.contents())
points.transform()
s = points.serialize()
print(s)
print(e.base64_to_float32(s['points']))

points2 = p.MultiPoint()
points2.deserialize(s)
print(points2.contents())

vv = points2.slice_to_grid(2)
for v in vv:
    sv = v.serialize()
    print(sv)
    print(e.base64_to_float32(sv['vertices']))


lines = p.MultiLine()
data = [[1, 5, 4, 6, 8, 4], [7, 8, 6, 2, 3, 4], [7, 8, 6, 4, 5, 2]]
for d in data:
    lines.push_l2(d)
print(lines.contents())
lines.transform()

for d in data:
    lines.push_l3(d)
print(lines.contents())
lines.transform()
s = lines.serialize()
print(s)
for l in s['lines']:
    print(e.base64_to_float32(l))

vv = lines.slice_to_grid(2)
for v in vv:
    sv = v.serialize()
    print(sv)
    print(e.base64_to_float32(sv['vertices']))

polygons = p.MultiPolygon()
data = [[0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1], [0.25, 0, 0.25, 0.75, 0, 0.25, 0.75, 0, 0.75, 0.25, 0, 0.75]], [[0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1]], [[0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]], [[0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1]]
for d in data:
    polygons.push_p3(d)
print(polygons.contents())
s = polygons.serialize()
print(s)
for o in s['polygons']:
    for r in o:
        print(e.base64_to_float32(r))

polygons.transform()
polygons2 = p.MultiPolygon()
polygons2.deserialize(s)
print(polygons2.contents())

#valgrind --tool=memcheck --track-origins=yes --leak-check=full --log-file=out.txt python test.py 
