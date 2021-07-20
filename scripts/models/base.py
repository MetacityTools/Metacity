from helpers.dirtree import DirectoryTreePaths

class Model:
    def __init__(self):
        pass


    def lod_exists(self, lod):
        return len(self.vertices[lod]) > 0

    
    def generate_lod_dict(self):
        return { lod: [] for lod in range(0, 6) }


    def export(self, paths: DirectoryTreePaths, oid):
        for lod in range(0, 6):
            if not self.lod_exists(lod):
                continue

            self.export_lod(paths, lod, oid)
