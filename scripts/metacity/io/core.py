import json

from metacity.models.model import FacetModel, NonFacetModel
from typing import Union, List, TextIO


def load_model(file: Union[str, TextIO]) -> Union[FacetModel, NonFacetModel]:
    try:
        contents = json.load(file)
    except:
        with open(file, 'r') as local_file:
            contents = json.load(local_file)
    
    if 'normals' in contents:
        model = FacetModel()
    else:
        model = NonFacetModel()
    model.deserialize(contents)
    return model 


def load_models(files: List[Union[str, TextIO]]) -> List[Union[FacetModel, NonFacetModel]]:
    models = []
    for file in files:
        models.append(load_model(file))
    return models




