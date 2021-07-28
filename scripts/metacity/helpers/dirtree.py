import os
import shutil

class DirectoryTreePaths:
    def __init__(self, output_dir):
        #dirs
        self.output = output_dir
        self.metadata = os.path.join(self.output, "metadata")
        self.geometry = os.path.join(self.output, "geometry")
        self.point_geometry = os.path.join(self.geometry, "points")
        self.line_geometry = os.path.join(self.geometry, "lines")
        self.facet_geometry = os.path.join(self.geometry, "facets")
        self.stl = os.path.join(self.output, "stl")
        self.all_dirs = [ self.output, self.metadata, 
                          self.geometry, self.point_geometry, 
                          self.line_geometry, self.facet_geometry, 
                          self.stl ]

        #files
        self.config = os.path.join(self.output, 'config.json')


    def recreate_tree(self):
        if os.path.exists(self.output):
            shutil.rmtree(self.output)
        for dir in self.all_dirs:
            os.mkdir(dir)


    def reconstruct_existing_tree(self):
        for dir in self.all_dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)


    def recreate_stl(self):
        if os.path.exists(self.stl):
            shutil.rmtree(self.stl)    
        os.mkdir(self.stl)


    @property
    def primitives(self):
        """List of primitive directories relative to self.geometry directory

        Returns:
            List[str]: List of directory names
        """
        return [f for f in os.listdir(self.geometry) if os.path.isdir(os.path.join(self.geometry, f))]


    def __primitive_type_lod_dirs(self, primitives):
        dirs = []
        for primitive in primitives:
            primitive_dir = os.path.join(self.geometry, primitive) 
            for lod_dir in os.listdir(primitive_dir):
                absolute_lod_dir = os.path.join(primitive_dir, lod_dir)
                if os.path.isdir(absolute_lod_dir):
                    dirs.append(os.path.join(primitive, lod_dir))
        return dirs


    @property
    def primitive_lods(self):
        """List of LODs inside primitives relative to self.geometry directory.

        Returns:
            List[str]: List of directory names
        """
        return self.__primitive_type_lod_dirs(self.primitives)


    @property
    def facet_lods(self):
        """List if LODs inside facet directory relative to self.geometry directory.

        Returns:
            List[str]: List of directory names
        """
        return self.__primitive_type_lod_dirs(['facets'])


    def models_for_lods(self, lods):
        """Returns list of paths to individual models for supplied LODs.
        The LODs are specified relatively to self.geometry (geometry) directory.

        Args:
            lod_dirs (List[str] or str): List of requested LOD directories relative to geometry directory.

        Returns:
            List[str]: List of paths to model files for requested LODs, path is relative to project root
        """

        if isinstance(lods, str):
            lod_dirs = [lods]

        model_files = []
        for lod in lod_dirs:
            lod_dir = os.path.join(self.geometry, lod)
            for object_file in os.listdir(lod_dir):
                absolute_object_file = os.path.join(lod_dir, object_file)
                if os.path.isfile(absolute_object_file):
                    model_files.append(absolute_object_file)
        return model_files


    def use_directory(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)
        return dir
