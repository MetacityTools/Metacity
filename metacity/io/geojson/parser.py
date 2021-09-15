import numpy as np
from metacity.datamodel.layer.layer import MetacityLayer
from metacity.filesystem import layer as fs
import geojson
from tqdm import tqdm





def parse(layer: MetacityLayer, input_file: str):
    with open(input_file, 'r') as file:
        contents = geojson.load(file)

    print(contents)