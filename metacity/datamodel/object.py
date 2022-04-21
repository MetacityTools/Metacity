from typing import List
from metacity.geometry import BaseModel


class Object:
    def __init__(self):
        self.meta = {}
        self.geometry: List[BaseModel] = []


        
