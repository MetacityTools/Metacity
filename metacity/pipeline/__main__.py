import metacity.pipeline.ui as ui
from metacity.io import parse_recursively
from metacity.geometry import Layer


if __name__ == "__main__":
    ui.print_intro_bar("metacity.pipeline", "Geodata Processing Pipeline", "Python")
    ui.print_message(f"""
    This script will help you get ready 
    your datasets for visualization.
    """)

    ui.prompt_task("1) Specify a dataset directory")
    dataset = ui.get_path(">>> ")
    ui.processing_sequence_start()
    models = parse_recursively(dataset)
    layer = Layer()
    layer.add_models(models)
    ui.processing_sequence_end()

    ui.prompt_task("2) Use envelope simplification?")



