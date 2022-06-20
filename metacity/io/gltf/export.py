from typing import Iterable
from metacity.datamodel.object import Object


def export_gltf(output_file: str, objects: Iterable[Object]):
    """
    Export a list of objects to a glTF file.

    Args:
        output_file (str): The file to export to.
        objects (Iterable[Object]): The objects to export.
    """

    nodes = []
    meshes = []
    for object in objects:
        data = 