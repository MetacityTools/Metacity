import metacity.geometry.primitive as p
import metacity.utils.encoding as e
from pprint import pprint as print
import matplotlib.pyplot as plt

polygons = p.MultiPolygon()
data = [[[0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1], [0.25, 0.25, 0.25, 0.75, 0.25, 0.25, 0.75, 0.75, 0.75, 0.25, 0.75, 0.75]]]

data3 = [[0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1]]
data2 = [[0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0]], [[0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1]]
print("adding")
for d in data:
    polygons.push_p3(d)

print("triangulating")
polygons.transform()

print("serializing")
s = polygons.serialize()
#print(s)
#for o in s['polygons']:
#    for r in o:
#        print(e.base64_to_float32(r))

polygons2 = p.MultiPolygon()
print("deserializing")
polygons2.deserialize(s)

print("slicing")
simples = polygons2.transform()
slices = simples.slice_to_grid(0.5)
print(len(slices))
for v in slices:
    print(v.centroid)

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

plt.figure()
vvv = []
for v in slices:
    sv = v.serialize()
    verts = e.base64_to_float32(sv['vertices'])
    verts = verts.reshape(verts.shape[0] // 9, 3, 3)
    for t in verts:
        vvv.append(t[:,[0, 2]])

cmap = get_cmap(len(vvv))
for i, t in enumerate(vvv):
    t2 = plt.Polygon(t, color=(*(cmap(i))[:3], 0.1), )
    plt.gca().add_patch(t2)

plt.show()
#valgrind --tool=memcheck --track-origins=yes --leak-check=full --log-file=out.txt python test.py 
