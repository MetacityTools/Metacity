from metacity.datamodel.project import Project
from metacity.core.grid.grid import Grid
from metacity.geometry import MeshOIDMapper
from tqdm import tqdm

p = Project("Praha")
source = p.get_layer("Obyvatelstvo")
target = p.get_layer("Budovy")
attribute = "Sum_PTOTAL"


for o in tqdm(target.objects):
    if attribute in o.meta:
        del o.meta[attribute]

grid = Grid(target)
tiles = [tile.polygon for tile in tqdm(grid.tiles) if tile.polygon is not None]

mapper = MeshOIDMapper(tiles)

grid = Grid(source)
for tile in tqdm(grid.tiles):
    p = tile.polygon
    if p is None:
        continue
    
    mapper.map_oids(p)

#target oid -> source oid
mapping = mapper.mapping
raw_mapping = mapper.raw_mapping
with open("oid_map.txt", "w") as f:
    for oid, source_oid in tqdm(raw_mapping.items()):
        f.write("{} {}\n".format(oid, source_oid))

target_objects = [ key for key in mapping.keys() ]
target_objects.sort()

for toid in tqdm(target_objects):
    source_oid = mapping[toid]
    m = source[source_oid].meta
    if attribute in m:
        target[toid].meta[attribute] = m[attribute]
target.persist()
