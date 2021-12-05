from metacity.datamodel.project import Project
from metacity.geometry import LegoBuilder
from metacity.core.grid.grid import Grid
from metacity.filesystem.base import write_json
from tqdm import tqdm

project = Project("Praha")
print(project)

#start = (-743663, -1042718)
#end = (-739792, -1040145)

start = [-742103, -1042204]
end = [-740323, -1040424]

xrange = (start[0] // 1000, (end[0] // 1000) + 1)
yrange = (start[1] // 1000, (end[1] // 1000) + 1)

tiles = [ (x, y) for x in range(*xrange) for y in range(*yrange) ]
print(tiles)

resolution = (xrange[1] - xrange[0], yrange[1] - yrange[0])
print(resolution)

builder = LegoBuilder()


for xy in tqdm(tiles):
    for layer in project.layers:
        grid = Grid(layer)
        tile = grid[xy]
        if tile is None:
            continue
        polygon = tile.polygon
        if polygon is not None:
            builder.insert_model(polygon)


print("building")
builder.build_heightmap(start[0], start[1], end[0], end[1], 2)

for i in tqdm(range(5, 45, 5)):
    config = builder.legofy(i)
    write_json(f"lego{i}.json", config)
    builder.lego_to_png(f"layout{i}.png")