
from metacity.grid.build import build_grid
import metacity.datamodel.project as proj
import metacity.io.load as load
import numpy as np

from metacity.io.stl.export import export_object

project = proj.MetacityProject("project")
l = project.get_layer("layer")
#build_grid(l, 1000)
#load.load(l, "/home/vojtatom/Desktop/TER_Prah56_polygonZ/TER_Prah56.shp")

#bbox = l.bbox
#print(bbox)
#with open("terrain.stl", 'w') as stl:
#    for object in l.objects:
#        export_object(object, stl)



#bbox = np.array(bbox) + np.array([-740000.0, -1054000.0, 272.2340087890625])
#print(bbox)
