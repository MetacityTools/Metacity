import metacity.pipeline.ui as ui
from metacity.io import parse_recursively
from metacity.geometry import Layer, Grid
from metacity.utils.filesystem import recreate_dir
import os


if __name__ == "__main__":
    ui.print_intro_bar("metacity.pipeline", "Geodata Processing Pipeline", "dev")
    ui.print_message(f"This script will help you get your datasets ready for visualization.")

    ui.prompt_task("1) Load data")
    while True:
        path = ui.get_path("Specify a dataset directory")
        datasets, extr_count = ui.count_datasets(path)
        if ui.confirm_dataset_selection(datasets, extr_count):
            break

    ui.processing_sequence_start()
    models = parse_recursively(path)
    layer = Layer()
    layer.add_models(models)
    ui.processing_sequence_end()

    if ui.get_yes_no("Use envelope simplification?"):
        ui.processing_sequence_start()
        layer.simplify_envelope()
        ui.processing_sequence_end()

    ui.prompt_task("2) Transform to Grid")
    while True:
        tile_size = ui.get_number("Specify a size of the grid tile")
        if ui.confirm_tile_size(tile_size):
            break

    ui.processing_sequence_start()
    grid = Grid(tile_size, tile_size)
    grid.add_layer(layer)
    ui.processing_sequence_end()

    if ui.get_yes_no("Merge models in tiles?"):
        ui.processing_sequence_start()
        grid.tile_merge()
        ui.processing_sequence_end()

    ui.prompt_task("3) Export")
    while True:
        path = ui.get_path("Specify a directory for grid export")
        if ui.validate_path(path):
            break
    
    ui.processing_sequence_start()
    recreate_dir(path)
    grid.to_gltf(path)
    ui.processing_sequence_end()

    ui.print_message(f"Your data has been prepared for visualization, you can find it in:")
    print(f"\n    {os.path.abspath(path)}")
    ui.print_message(f"Thank you for using metacity.pipeline!")
    print()


    


