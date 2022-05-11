from metacity.datamodel.object import Object
from typing import List

class Layer:
    def __init__(self, name):
        """
        Initialize a layer. Layer represents a collection of objects.
        
        Args:
            name (str): The name of the layer.
        """
        self.name = name
        self.objects = []
    
    def add_object(self, obj: Object):
        """
        Add an object to the layer.
        
        Args:
            obj (Object): The object to add.
        """
        self.objects.append(obj)

    def add_objects(self, objs: List[Object]):
        """
        Add objects to the layer. 

        Args:
            objs (List[Object]): The objects to add.
        """
        self.objects.extend(objs)