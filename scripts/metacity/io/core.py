import json
from metacity.models.model import FacetModel, NonFacetModel


def load_model(file):
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


def load_models(files):
    models = []
    for file in files:
        models.append(load_model(file))
    return models
