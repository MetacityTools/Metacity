import argparse
import metacity.utils.filesystem as fs
import metacity.io as io
import metacity.geometry as mg 
from metacity.processor.config import Config


def load_layer(config: Config):
    models = io.parse(config.input)
    if models is None:
        raise ValueError("No models were loaded")
    print(f"Loaded {len(models)} models")
    layer = mg.Layer(models)
    return layer


def export_tree(config: Config, layer: mg.Layer):
    treeConfig = config.tree

    print(f"Building tree with config: {treeConfig.config}")
    tree = mg.QuadTree(layer, treeConfig.aggregate_mode, treeConfig.max_depth)
    if treeConfig.merge_tiles:
        print("Merging tiles")
        tree.merge_at_level(treeConfig.tile_level)
    
    print(f"Writing tree to {config.output}")
    fs.recreate_dir(config.output)

    if treeConfig.keep_keys is not None:
        print(f"Keeping keys: {treeConfig.keep_keys}")
        tree.filter_metadata(treeConfig.keep_keys)

    tree.to_json(config.output, treeConfig.tile_level)


def apply_modifiers(config: Config, layer: mg.Layer):
    if config.simplify:
        print("Simplifying models")
        layer.simplify_envelope()

    if config.move_to_plane_z is not None:
        print(f"Moving models to plane z: {config.move_to_plane_z}")
        layer.move_to_plane_z(config.move_to_plane_z)

    if config.map_to_layer is not None:
        print(f"Mapping models to layer: {config.map_to_layer}")
        mapLayer = load_layer(config.map_to_layer)
        layer.map_to_layer(mapLayer)


def apply(config: Config):
    print(f"Applying config {config}")
    layer = load_layer(config)
    apply_modifiers(config, layer)
    export_tree(config, layer)


def parse_config(config_file: str):
    print(f"Parsing config file {config_file}")
    config = fs.read_json(config_file)
    return Config(config)


def validate(config_file: str):
    if not config_file:
        raise ValueError("config_file must be specified")

    if not fs.file_exists(config_file):
        raise ValueError(f"config_file {config_file} does not exist")

    if not fs.readable(config_file):
        raise ValueError(f"config_file {config_file} is not readable")


def process(config_file: str):
    print(f"Processing with {config_file}")
    validate(config_file)
    config = parse_config(config_file)
    apply(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Metacity Processor')
    parser.add_argument('--config', type=str, required=True, help='Config file')
    args = parser.parse_args()
    process(args.config)