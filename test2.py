import metacity.geometry.primitive as p
import metacity.utils.encoding as e
from pprint import pprint as print

lines = p.MultiLine()
data = [[1, 5, 4, 6, 8, 4], [7, 8, 6, 2, 3, 4], [7, 8, 6, 4, 5, 2]] * 1000000
for d in data:
    lines.push_l2(d)
#print(lines.contents())
print("loaded")
lines.transform()
print("transformed")
for d in data:
    lines.push_l3(d)
print("loaded")
lines.transform()
print("transformed")
s = lines.serialize()
print("serialized")
#for l in s['lines']:
#    print(e.base64_to_float32(l))

vv = lines.slice_to_grid(2)
print("sliced")
#print(vv)
#for v in vv:
#    sv = v.serialize()
#    print(e.base64_to_float32(sv['vertices']))
