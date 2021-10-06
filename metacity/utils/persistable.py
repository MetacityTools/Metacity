from metacity.filesystem.file import read_json, write_json
from abc import ABC, abstractmethod


class Persistable(ABC):
    def __init__(self, files):
        if isinstance(files, list) or isinstance(files, tuple):
            self.files = files
        else:
            self.files = [files]

    @abstractmethod
    def serialize():
        pass

    @abstractmethod
    def deserialize():
        pass

    def load(self):
        data = []
        for file in self.files:
            data.append(read_json(file))
        self.deserialize(**data)

    def export(self):
        data = self.serialize()
        if not (isinstance(data, list) or isinstance(data, tuple)):
            data = [data]

        if len(data) != len(self.files):
            raise Exception(f"Mismatch in number of serialization files {len(self.files)} and data instances {len(data)}")
        
        for d, f in zip(data, self.files):
            write_json(f, d)