from metacity.filesystem.base import read_json, write_json
from abc import ABC, abstractmethod


class Persistable(ABC):
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def serialize():
        pass

    @abstractmethod
    def deserialize():
        pass

    def load(self):
        data = read_json(self.file)
        self.deserialize(data)

    def export(self):
        data = self.serialize()
        write_json(self.file, data)