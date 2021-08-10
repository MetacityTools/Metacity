import os
from metacity.helpers.file import id_from_filename
import shutil

class RelativePaths:
    def __init__(self):
        self.metadata = "metadata"
        self.geometry = "geometry"
        self.point_geometry = os.path.join(self.geometry, "points")
        self.line_geometry = os.path.join(self.geometry, "lines")
        self.facet_geometry = os.path.join(self.geometry, "facets")
        self.tiles = "tiles"
        self.point_tiles = os.path.join(self.tiles, "points")
        self.line_tiles = os.path.join(self.tiles, "lines")
        self.facet_tiles = os.path.join(self.tiles, "facets")
        self.all_dirs = [ self.metadata, 
                          self.geometry, 
                          self.point_geometry, self.line_geometry, self.facet_geometry,  
                          self.tiles, 
                          self.point_tiles, self.line_tiles, self.facet_tiles ]

        self.dirs_geometry = [
            self.point_geometry, self.line_geometry, self.facet_geometry
        ]
        
        self.dirs_tiles = [
            self.point_tiles, self.line_tiles, self.facet_tiles
        ]

        self.dirs_with_lods = [
            self.point_geometry, self.line_geometry, self.facet_geometry,
            self.point_tiles, self.line_tiles, self.facet_tiles
        ]  


def create_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


class LayerDirectoryTree:
    def __init__(self, layer_name, project_dir):
        self.project_dir = project_dir
        self.base = os.path.join(project_dir, layer_name)
        self.rel = RelativePaths()


    def recreate_layer(self, load_existing=True):
        if os.path.exists(self.base) and not load_existing:
            shutil.rmtree(self.base)
        
        create_dir_if_not_exists(self.project_dir)
        create_dir_if_not_exists(self.base)

        for dir in self.rel.all_dirs:
            create_dir_if_not_exists(os.path.join(self.base, dir))

        for dir in self.rel.dirs_with_lods:
            for i in range(0, 5):
                create_dir_if_not_exists(os.path.join(self.base, dir, str(i)))


    def __primitive_lod_dir(self, primitive, lod):
        return os.path.join(self.base, primitive, str(lod))
    
    
    def __primitive_lod_dirs(self, primitive):
        return [ self.__primitive_lod_dir(primitive, i) for i in range(0, 5) ]


    @property
    def point_geometry_lod_dirs(self):
        return self.__primitive_lod_dirs(self.rel.point_geometry)


    def point_geometry_lod_dir(self, lod):
        return self.__primitive_lod_dir(self.rel.point_geometry, lod)


    @property
    def point_tiles_lod_dirs(self):
        return self.__primitive_lod_dirs(self.rel.point_tiles)


    def point_tiles_lod_dir(self, lod):
        return self.__primitive_lod_dir(self.rel.point_tiles, lod)


    @property
    def line_geometry_lod_dirs(self):
        return self.__primitive_lod_dirs(self.rel.line_geometry)
 

    def line_geometry_lod_dir(self, lod):
        return self.__primitive_lod_dir(self.rel.line_geometry, lod)


    @property
    def line_tiles_lod_dirs(self):
        return self.__primitive_lod_dirs(self.rel.line_tiles)
 

    def line_tiles_lod_dir(self, lod):
        return self.__primitive_lod_dir(self.rel.line_tiles, lod)


    @property
    def facet_geometry_lod_dirs(self):
        return self.__primitive_lod_dirs(self.rel.facet_geometry)


    def facet_geometry_lod_dir(self, lod):
        return self.__primitive_lod_dir(self.rel.facet_geometry, lod)

    
    @property
    def facet_tiles_lod_dirs(self):
        return self.__primitive_lod_dirs(self.rel.facet_tiles)


    def facet_tiles_lod_dir(self, lod):
        return self.__primitive_lod_dir(self.rel.facet_tiles, lod)


    @property
    def all_geometry_lod_dirs(self):
        return [ os.path.join(self.base, dir, str(i)) for i in range(0, 5) for dir in self.rel.dirs_geometry ]



    @property
    def all_tiles_lod_dirs(self):
        return [ os.path.join(self.base, dir, str(i)) for i in range(0, 5) for dir in self.rel.dirs_tiles ]


    @property
    def metadta_dir(self):
        return os.path.join(self.base, self.rel.metadata)


    def metadata_for_oid(self, oid: str):
        return os.path.join(self.metadta_dir, oid + 'json')


    @property
    def any_object_exists(self):
        for dir in self.all_geometry_lod_dirs:
            for _ in os.listdir(dir):
                return True
        return False


    @property
    def object_ids(self):
        objects = set()
        for dir in self.all_geometry_lod_dirs:
            for o in os.listdir(dir):
                oid = id_from_filename(o)
                if oid not in objects:
                    objects.add(oid)
        return list(objects)


    @property
    def config(self):
        return os.path.join(self.base, 'config.json')


    @property
    def grid(self):
        return os.path.join(self.base, 'grid.json')

    






    @staticmethod
    def layer_dirs(project_dir):
        return [ d for d in os.listdir(project_dir) ]


