from metacity.filesystem import styles as fs
from metacity.utils.encoding import npuint8_to_buffer


class ProjectStyleSet:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.layer_sets = {}

    def get_style(self, name: str):
        file = fs.style_mss(self.project_dir, name)
        return fs.base.read_mss(file)

    def update_style(self, name: str, mss: str):
        file = fs.style_mss(self.project_dir, name)
        dir = fs.style_dir(self.project_dir, name)
        fs.base.write_mss(file, mss)
        fs.base.recreate_dir(dir)

    def list_styles(self):
        return fs.list_styles(self.project_dir)

    def add_style(self, name: str, layer_name: str, buffer):
        file = fs.style_buffer(self.project_dir, layer_name, name)
        style = {
            'buffer': npuint8_to_buffer(buffer)
        }
        fs.base.write_json(file, style)

    def add_overlay_style(self, name: str, layer_name: str, buffer_source, buffer_target):
        file = fs.style_buffer(self.project_dir, layer_name, name)
        style = {
            'buffer_source': npuint8_to_buffer(buffer_source),
            'buffer_target': npuint8_to_buffer(buffer_target)
        }
        fs.base.write_json(file, style)

    def rename_style(self, name: str, new_name: str):
        file = fs.style_mss(self.project_dir, name)
        dir = fs.style_dir(self.project_dir, name)
        new_file = fs.style_mss(self.project_dir, new_name)
        new_dir = fs.style_dir(self.project_dir, new_name)
        fs.base.rename(file, new_file)
        fs.base.rename(dir, new_dir)

    def delete_style(self, name: str):
        file = fs.style_mss(self.project_dir, name)
        dir = fs.style_dir(self.project_dir, name)
        fs.base.delete_file(file)
        fs.base.delete_dir(dir)

    def build_layout(self):
        return self.list_styles()
