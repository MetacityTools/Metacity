import metacity.geometry as mg 


class ConfigBase:
    def __init__(self, config: dict):
        self.config = config

    def prop_default(self, property: str, default = None, required = False):
        if property not in self.config:
            if required and (default is None):
                raise ValueError("Missing required property: " + property)
            else:
                return default
        return self.config[property]


class TreeConfig(ConfigBase):
    def __init__(self, config: dict):
        super().__init__(config)

    @property
    def max_depth(self):
        return self.prop_default("max_depth", default=10)

    @property
    def tile_level(self):
        return self.prop_default("tile_level", default=5)

    @property
    def aggregate_mode(self):
        mode = self.prop_default("aggregate_mode", default="MAX_AREA")
        if mode == "MAX_AREA":
            return mg.MetadataMode.MAX_AREA
        elif mode == "AVERAGE":
            return mg.MetadataMode.AVERAGE
        else:
            raise ValueError("Invalid aggregate mode: " + mode)

    @property
    def merge_tiles(self):
        return self.prop_default("merge_tiles", default=False)

    @property
    def keep_keys(self):
        return self.prop_default("keep_keys")



class Config(ConfigBase):
    def __init__(self, config: dict):
        super().__init__(config)

    def prop_default(self, property: str, default = None, required = False):
        if property not in self.config:
            if required and (default is None):
                raise ValueError("Missing required property: " + property)
            else:
                return default
        return self.config[property]

    @property
    def input(self):
        return self.prop_default("input", required=True)

    @property
    def output(self):
        return self.prop_default("output", required=True)

    @property
    def simplify(self):
        return self.prop_default("simplify", default=False)

    @property
    def move_to_plane_z(self):
        return self.prop_default("move_to_plane_z")

    @property
    def map_to_layer(self):
        return self.prop_default("map_to_layer")

    @property
    def tree(self):
        return TreeConfig(self.prop_default("tree", default={}))