


def desermodel(model):
    return None


class Object:
    def __init__(self):
        self.meta = {}
        self.models = []

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
        
