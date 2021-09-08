from metacity.utils.sorter import GridSorter
import numpy as np
from metacity.datamodel.primitives.base import BaseModel
from metacity.utils.slicing import split_line
import numpy as np


class LineModel(BaseModel):
    TYPE = "lines"

    def __init__(self):
        super().__init__()

    @property
    def items(self):
        vert = self.buffers.vertices.reshape((self.buffers.vertices.shape[0] // 6, 2, 3))
        sema = self.buffers.semantics.reshape((self.buffers.semantics.shape[0] // 2, 2))

        for segment, semantic in zip(vert, sema):
            yield segment, semantic

    @property
    def deepcopy(self):
        model = LineModel()
        self.deepcopy_into(model)
        return model

    @property
    def deepcopy_nobuffers(self):
        model = LineModel()
        self.deepcopy_into_nobuffers(model)
        return model

    def split(self, x_planes, y_planes):
        v, s = [], []
        for segment, semantic in self.items:
            segments = split_line(segment, x_planes, y_planes)
            v.extend(segments)
            s.extend(np.repeat([semantic], len(segments), axis=0))
        model = LineModel()
        self.set_meta_copy(model, v, s)
        return model.__splitsort(x_planes, y_planes)
    
    def __splitsort(self, x_planes, y_planes):
        grid = GridSorter(x_planes, y_planes)
        for seg, sem in self.items:
            center = np.sum(seg, axis=0) / 2
            grid.insert((seg, sem), center)
        models = []
        for elements in grid.partitions.values():
            seg, sem = [], []
            for element in elements:
                seg.append(element[0])
                sem.append(element[1])
            model = LineModel()
            self.set_meta_copy(model, seg, sem)
            models.append(model)
        return models

