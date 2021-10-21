from typing import Callable, Dict, List
from metacity.geometry import MultiPoint, MultiLine, MultiPolygon, Primitive

types: Dict[str, Callable[[],Primitive]] = {
    MultiPoint().type: MultiPoint,
    MultiLine().type: MultiLine,
    MultiPolygon().type: MultiPolygon
}

def desermodel(model):
    type = model["type"]
    if model["type"] in types:
        m = types[type]()
    else:
        raise RuntimeError(f"Unknown model type: {type}")
    m.deserialize(model)
    return m


class Object:
    def __init__(self):
        self.meta = {}
        self.models: List[Primitive] = []

    def serialize(self):
        models = []
        for model in self.models:
            models.append(model.serialize())

        return {
            'meta': self.meta,
            'models': models
        }

    def deserialize(self, models, meta):
        self.meta = meta
        for model in models:
            self.models.append(desermodel(model))
        
