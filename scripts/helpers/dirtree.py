import os
import shutil

class DirectoryTreePaths:
    def __init__(self, output_dir):
        self.output = output_dir
        self.objects = os.path.join(self.output, "objects")
        self.geometry = os.path.join(self.output, "geometry")
        self.point_geometry = os.path.join(self.geometry, "points")
        self.line_geometry = os.path.join(self.geometry, "line")
        self.facet_geometry = os.path.join(self.geometry, "facets")


    def recreate_tree(self):
        if os.path.exists(self.output):
            shutil.rmtree(self.output)
        os.mkdir(self.output)
        os.mkdir(self.objects)
        os.mkdir(self.geometry)
        os.mkdir(self.point_geometry)
        os.mkdir(self.line_geometry)
        os.mkdir(self.facet_geometry)


    def use_lod_directory(self, base, lod):
        lod_dir = os.path.join(base, str(lod))
        if not os.path.exists(lod_dir):
            os.mkdir(lod_dir)
        return lod_dir


    def use_points_lod_directory(self, lod):
        return self.use_lod_directory(self.point_geometry, lod)


    def use_line_lod_directory(self, lod):
        return self.use_lod_directory(self.line_geometry, lod)


    def use_facet_lod_directory(self, lod):
        return self.use_lod_directory(self.facet_geometry, lod)