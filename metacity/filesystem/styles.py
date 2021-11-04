import os
from metacity.filesystem import base
from metacity.filesystem import layer


def style_mss(project_dir, style_name):
    return os.path.join(layer.project_styles(project_dir), f'{style_name}.mss')


def style_dir(project_dir, style_name):
    return os.path.join(layer.project_styles(project_dir), style_name)


def style_buffer(project_dir, layer_name, style_name):
    return os.path.join(style_dir(project_dir, style_name), f'{layer_name}.json')


def list_styles(project_dir):
    dir = layer.project_styles(project_dir)
    return [ s for s in os.listdir(dir) if os.path.isdir(os.path.join(dir, s)) ]

