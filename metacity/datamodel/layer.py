from metacity.datamodel.object import Object
from typing import List

class Layer:
    def __init__(self, name):
        self.name = name
        self.objects = []
    
    def add_object(self, obj: Object):
        self.objects.append(obj)

    def add_objects(self, objs: List[Object]):
        self.objects.extend(objs)