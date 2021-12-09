from metacity.filesystem import styles as fs
from metacity.utils.encoding import npuint8_to_buffer
from metacity.datamodel.project import Project


class Style:
    def __init__(self, project: Project, name: str):
        self.project = project
        self.project_dir = project.dir
        self.name = name

    @staticmethod
    def list(project: Project):
        return fs.list_styles(project.dir)

    @staticmethod
    def create(project: Project, name: str):
        if fs.base.file_exists(fs.style_mss(project.dir, name)):
            return False
        style = Style(project, name)
        style.update('')
        return True

    @property
    def style_file(self):
        file = fs.style_mss(self.project_dir, self.name)
        return fs.base.read_mss(file)

    def add_legend(self, rules: dict):
        file = fs.style_legend(self.project_dir, self.name)
        fs.base.write_json(file, rules)

    def update(self, mss: str):
        file = fs.style_mss(self.project_dir, self.name)
        dir = fs.style_dir(self.project_dir, self.name)
        fs.base.write_mss(file, mss)
        fs.base.recreate_dir(dir)

    def write_colors(self, layer_name: str, buffer=None, buffer_source=None, buffer_target=None):
        if buffer is not None:
            file = fs.style_buffer(self.project_dir, layer_name, self.name)
            style = {
                'buffer': npuint8_to_buffer(buffer)
            }
            fs.base.write_json(file, style)
        elif buffer_source is not None and buffer_target is not None:
            file = fs.style_buffer(self.project_dir, layer_name, self.name)
            style = {
                'buffer_source': npuint8_to_buffer(buffer_source),
                'buffer_target': npuint8_to_buffer(buffer_target)
            }
            fs.base.write_json(file, style)

    def rename(self, new_name: str):
        file = fs.style_mss(self.project_dir, self.name)
        dir = fs.style_dir(self.project_dir, self.name)
        new_file = fs.style_mss(self.project_dir, new_name)
        new_dir = fs.style_dir(self.project_dir, new_name)
        if fs.base.rename(file, new_file):
            fs.base.rename(dir, new_dir)
            self.name = new_name
            return True
        return False

    def delete(self):
        file = fs.style_mss(self.project_dir, self.name)
        dir = fs.style_dir(self.project_dir, self.name)
        fs.base.delete_file(file)
        fs.base.delete_dir(dir)

