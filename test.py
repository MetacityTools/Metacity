import metacity.geometry.primitive as p
import metacity.utils.encoding as e
from pprint import pprint as print
import base64
points = p.MultiPoint()
data = [5, 6, 4, 8, 4, 6]
points.push_p2(data)
print(points.contents())
points.push_p3(data)
print(points.contents())

s = points.serialize()
print(s)
print(e.base64_to_float32(s['points']))

points2 = p.MultiPoint()
points2.deserialize(s)
print(points2.contents())


lines = p.MultiLine()
data = [[1, 5, 4, 6, 8, 4], [7, 8, 6, 2, 3, 4], [7, 8, 6, 4, 5, 2]]
for d in data:
    lines.push_l2(d)
print(lines.contents())

for d in data:
    lines.push_l3(d)
print(lines.contents())
s = lines.serialize()
print(s)
for l in s['lines']:
    print(e.base64_to_float32(l))

polygons = p.MultiPolygon()
data = [[1, 5, 4, 6, 8, 4, 7, 8, 9], [7, 8, 6, 2, 3, 4], [7, 8, 6, 4, 5, 2, 1, 2, 3]]
polygons.push_p3(data)
print(polygons.contents())
s = polygons.serialize()
print(s)
for o in s['polygons']:
    for r in o:
        print(e.base64_to_float32(r))

#valgrind --tool=memcheck --track-origins=yes --leak-check=full --log-file=out.txt python test.py 
