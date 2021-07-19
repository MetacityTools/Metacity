from helpers.dirtree import DirectoryTreePaths

class Model:
    def __init__(self):
        pass


    def lod_exists(self, lod):
        return len(self.vertices[lod]) > 0


    def export(self, paths: DirectoryTreePaths, oid):
        for lod in range(1, 6):
            if not self.lod_exists(lod):
                continue

            self.export_lod(paths, lod, oid)
