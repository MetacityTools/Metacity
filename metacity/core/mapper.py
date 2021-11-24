from metacity.datamodel.layer import Layer, Overlay

def build_overlay(self, source: Layer, target: Layer, iterationCallback=None):
    if source.type != "layer" or target.type != "layer":
        raise Exception(f"Cannot map type {source.type} to {target.type}, only layer to layer is supported")

    tg = Grid(target)
    sg = source.grid

    grid = self.grid

    it = 0
    for source_tile, target_tile in sg.overlay(tg):
        pol = target_tile.polygon
        if pol is None:
            continue
        
        for source_model in source_tile.objects:
            source_copy = source_model.copy()
            source_copy.map(pol)
            grid.tile_from_single_model(source_copy, source_tile.name)

        if iterationCallback is not None:
            iterationCallback(it)
            it += 1

    grid.persist() #persist with empy cache
    self.source_layer = source.name
    self.target_layer = target.name
    self.size_source = source.size
    self.size_target = target.size