from metacity.datamodel.models.levels import ModelLevels
from metacity.datamodel.models.primitives.facets import FacetModel
from tests.datamodel.models.primitives.test_facets import (init_random_model,
                                                           models_equal)
from tests.tree import geometry_tree  # it is accessed as param in test


def test_init():
    model = ModelLevels(FacetModel)
    assert len(model.lod.keys()) == 5
    assert model.primitive_class == FacetModel 
    assert model.type == FacetModel.TYPE


def init_random_model_lod():
    model = ModelLevels(FacetModel)
    for i in range(0, 4):
        model.lod[i] = init_random_model()
    return model


def test_import_export(geometry_tree):
    model = init_random_model_lod()

    oid = "testmodel"
    geometry_path = geometry_tree
    model.export(oid, geometry_path)
    
    model2 = ModelLevels(FacetModel)
    model2.load(oid, geometry_path)

    for lod in range(0, 5):
        models_equal(model.lod[lod], model2.lod[lod])


    