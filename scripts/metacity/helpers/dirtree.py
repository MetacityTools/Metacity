import os
from metacity.helpers.file import id_from_filename
import shutil

class RelativePaths:
    def __init__(self):
        self.metadata = "metadata"
        self.geometry = "geometry"
        self.points = "points"
        self.lines = "lines"
        self.facets = "facets"
        self.point_geometry = os.path.join(self.geometry, self.points)
        self.line_geometry = os.path.join(self.geometry, self.lines)
        self.facet_geometry = os.path.join(self.geometry, self.facets)
        self.grid = "grid"
        self.grid_cache = os.path.join(self.grid, "cache")
        self.grid_tiles = os.path.join(self.grid, "tiles")

        self.all_dirs = [ self.metadata, 
                          self.geometry, 
                          self.point_geometry, self.line_geometry, self.facet_geometry,  
                          self.grid,
                          self.grid_cache, self.grid_tiles ]

        self.dirs_geometry = [
            self.point_geometry, self.line_geometry, self.facet_geometry
        ]


        self.dirs_with_lods = [
            self.point_geometry, self.line_geometry, self.facet_geometry
        ]  


    @property
    def primitives(self):
        return [self.points, self.lines, self.facets]



def create_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def recreate_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    create_dir_if_not_exists(dir)


def recreate_lod_dirs(base):
    for i in range(0, 5):
        create_dir_if_not_exists(os.path.join(base, str(i)))



class LayerDirectoryTree:
    def __init__(self, layer_name, project_dir):
        self.project_dir = project_dir
        self.base = os.path.join(project_dir, layer_name)
        self.rel = RelativePaths()


    def recreate_layer(self, load_existing=True):
        create_dir_if_not_exists(self.project_dir)

        if load_existing:
            create_dir_if_not_exists(self.base)
        else:
            recreate_dir(self.base)

        for dir in self.rel.all_dirs:
            create_dir_if_not_exists(os.path.join(self.base, dir))

        for dir in self.rel.dirs_with_lods:
            recreate_lod_dirs(os.path.join(self.base, dir))


    def tile_name(self, x, y):
        return f'{x}_{y}'


    def recreate_tile(self, x, y):
        tile_name = self.tile_name(x, y)
        tile_base = os.path.join(self.base, self.rel.grid_tiles, tile_name)
        recreate_dir(tile_base)
        recreate_lod_dirs(tile_base)


    def recreate_tile_cache(self, tile_name):
        cache_base = os.path.join(self.base, self.rel.grid_cache, tile_name)
        recreate_dir(cache_base)

        for prim in self.rel.primitives:
            prim_path = os.path.join(cache_base, prim)
            create_dir_if_not_exists(prim_path)
            recreate_lod_dirs(prim_path)


    def recreate_cache(self):
        for tile in self.tile_names:
            self.recreate_tile_cache(tile)


    def clear_grid(self):
        grid = os.path.join(self.base, self.rel.grid)
        shutil.rmtree(grid)
        os.mkdir(grid)
        os.mkdir(os.path.join(self.base, self.rel.grid_cache))
        os.mkdir(os.path.join(self.base, self.rel.grid_tiles))


    @property
    def all_lod_dirs(self):
        return [ os.path.join(dir, str(i)) for i in range(0, 5) for dir in self.rel.primitives ]


    @property
    def metadta_dir(self):
        return os.path.join(self.base, self.rel.metadata)


    def metadata_for_oid(self, oid: str):
        return os.path.join(self.metadta_dir, oid + '.json')


    @property
    def any_object_exists(self):
        for dir in self.all_lod_dirs:
            for _ in os.listdir(os.path.join(self.base, self.rel.geometry, dir)):
                return True
        return False


    def objects(self, base_dir):
        oids = set()
        for dir in self.all_lod_dirs:
            for o in os.listdir(os.path.join(base_dir, dir)):
                oid = id_from_filename(o)
                if oid not in oids:
                    oids.add(oid)
                    yield oid


    @property
    def object_ids(self):
        base_dir = os.path.join(self.base, self.rel.geometry)
        return self.objects(base_dir)


    def objects_in_tile_cache(self, x, y):
        cache_dir = os.path.join(self.base, self.rel.grid_cache, self.tile_name(x, y))
        return self.objects(cache_dir)



    @property
    def geometry_object_dir(self):
        return os.path.join(self.base, self.rel.geometry)


    @property
    def cache_object_dir(self):
        return os.path.join(self.base, self.rel.grid_cache)


    @property
    def tile_names(self):
        for tile in os.listdir(os.path.join(self.base, self.rel.grid_tiles)):
            yield tile


    @property
    def config(self):
        return os.path.join(self.base, 'config.json')


    @property
    def grid_config(self):
        return os.path.join(self.base, self.rel.grid, 'grid.json')


    def tile_config(self, x, y):
        return os.path.join(self.base, self.rel.grid_tiles, self.tile_name(x, y), 'config.json')


    def tile_dir(self, x, y):
        return os.path.join(self.base, self.rel.grid_tiles, self.tile_name(x, y))


    @staticmethod
    def layer_dirs(project_dir):
        return [ d for d in os.listdir(project_dir) ]







