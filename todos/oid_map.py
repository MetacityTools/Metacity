from metacity.datamodel.project import Project
from metacity.core.mapper import bbox_attribute_mapping
from tqdm import tqdm

p = Project("Praha")
source = p.get_layer("Obyvatelstvo")
target = p.get_layer("Budovy")
count = "Sum_PTOTAL"
area = "Shape_Area"
attributes = [count, area]
bbox_attribute_mapping(source, target, attributes)

maximum = 0
avg = 0
cnt = 0

for o in tqdm(target.objects):
    if count in o.meta and area in o.meta:
        o.meta[count] = o.meta[count] / o.meta[area]
        avg += o.meta[count]
        cnt += 1
        maximum = max(maximum, o.meta[count])

print(maximum)
maximum /= 1000

for o in tqdm(target.objects):
    if count in o.meta and area in o.meta:
        o.meta[count] /= maximum

avg = avg / cnt
print(avg * 1000)

target.persist()
