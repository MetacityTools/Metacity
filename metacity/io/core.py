import json

from metacity.models.model import FacetModel, LineModel, PointModel
from metacity.models.tiles.model import TileModel
from typing import Union, List, TextIO


def load_model(file: Union[str, TextIO]) -> Union[FacetModel, LineModel, PointModel]:
    try:
        contents = json.load(file)
    except:
        with open(file, 'r') as local_file:
            contents = json.load(local_file)
    
    type = contents['type']
    if type == PointModel.json_type:
        model = PointModel()
    elif type == LineModel.json_type:
        model = LineModel()
    elif type == FacetModel.json_type:
        model = FacetModel()
    else:
        raise Exception(f'Unknown model type: "{type}"')

    model.deserialize(contents)
    return model 


def load_models(files: List[Union[str, TextIO]]) -> List[Union[FacetModel, LineModel, PointModel]]:
    models = []
    for file in files:
        models.append(load_model(file))
    return models


def load_tile(file: Union[str, TextIO]) -> Union[FacetModel, LineModel, PointModel]:
    try:
        contents = json.load(file)
    except:
        with open(file, 'r') as local_file:
            contents = json.load(local_file)


    type = contents['type']
    if type == PointModel.json_type:
        tile = TileModel(PointModel)
    elif type == LineModel.json_type:
        tile = TileModel(LineModel)
    elif type == PointModel.json_type:
        tile = TileModel(FacetModel)
    else:
        raise Exception(f'Unknown model type: "{type}"')

    tile.deserialize(contents)
    return tile 
    