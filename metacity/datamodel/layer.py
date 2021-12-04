from metacity.datamodel.object import Object
from metacity.datamodel.set import ObjectSet
from metacity.filesystem import layer as fs
from metacity.utils.persistable import Persistable


class Layer(Persistable):
    def __init__(self, layer_dir: str, group_by = 100000, load_set=True, load_meta=True, load_model=True):
        super().__init__(fs.layer_config(layer_dir))

        self.dir = layer_dir
        self.size = 0
        self.group_by = group_by
        self.disabled = False

        fs.create_layer(self.dir)
        self.load_meta = load_meta
        self.load_model = load_model

        try:
            self.load()
        except FileNotFoundError:
            self.export()

        if load_set:
            self.set = ObjectSet(self.dir, 0, self.group_by, load_meta=load_meta, load_model=load_model)
        else:
            self.set = None
    
    @property
    def type(self):
        return "layer"

    @property
    def name(self):
        return fs.layer_name(self.dir)

    def add(self, object: Object):
        if not self.set.can_contain(self.size):
            self.set.export()
            self.activate_set(self.size)
        self.set.add(object)
        self.size += 1

    def persist(self):
        self.export()
        self.set.export()

    def __getitem__(self, index: int):
        if not self.set.can_contain(index):
            self.set.export()
            self.activate_set(index)
        obj = self.set[index]
        return obj

    def activate_set(self, index):
        offset = (index // self.group_by) * self.group_by
        self.set = ObjectSet(self.dir, offset, self.group_by, load_meta=self.load_meta, load_model=self.load_model)

    def regroup(self, group_by):
        tmp = fs.layer_regrouped(self.dir)
        fs.remove(tmp)

        regrouped = Layer(tmp, group_by)
        for o in self.objects:
            regrouped.add(o)

        regrouped.persist()
        fs.move_from_regrouped(self.dir)
        self.group_by = group_by
        self.export()

    @property
    def objects(self):
        for i in range(self.size):
            yield self[i]

    def add_source_file(self, source_file_path: str):
        return fs.copy_to_layer(self.dir, source_file_path)

    def serialize(self):
        return {
            'type': 'layer',
            'size': self.size,
            'group_by': self.group_by,
            'disabled': self.disabled
        }

    def deserialize(self, data):
        self.size = data['size']
        self.group_by = data['group_by']
        self.disabled = data['disabled']

    def clear(self, keep_originals=True):
        if not self.load_model or not self.load_meta:
            raise Exception("In order to clear layer properly, loading models and metadata must be enabled.")
        
        fs.clear_layer(self.dir, keep_originals)
        self.size = 0
        self.set = ObjectSet(self.dir, 0, self.group_by)


class LayerOverlay(Persistable):
    def __init__(self, overlay_dir: str):
        super().__init__(fs.layer_config(overlay_dir))
        self.source_layer = None
        self.target_layer = None
        self.dir = overlay_dir
        self.disabled = False
        self.size_source = 0
        self.size_target = 0
        fs.create_overlay(self.dir)

        try:
            self.load()
        except FileNotFoundError:
            self.export()

    @property
    def type(self):
        return "overlay"

    @property
    def name(self):
        return fs.layer_name(self.dir)

    @property
    def size(self):
        return [self.size_source, self.size_target]

    def persist(self):
        self.export()

    def serialize(self):
        return {
            'type': 'overlay',
            'disabled': self.disabled,
            'source': self.source_layer,
            'target': self.target_layer,
            'size_source': self.size_source,
            'size_target': self.size_target
        }

    def deserialize(self, data):
        self.source_layer = data['source']
        self.target_layer = data['target']
        self.disabled = data['disabled']
        self.size_source = data['size_source']
        self.size_target = data['size_target']


    def clear(self, keep_originals=True):
        fs.clear_overlay(self.dir, keep_originals)
        self.size_source = 0
        self.size_target = 0

