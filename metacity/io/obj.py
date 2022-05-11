from typing import Iterable
from metacity.datamodel.object import Object



def export_obj(output_file: str, objects: Iterable[Object]):
    """
    Export objects to an OBJ file.

    Args:
        output_file (str): The file to export to.
        objects (Iterable[Object]): The objects to export.
    
    Returns:
        int: The number of vertices exported.
    """
    written_verts = 0
    for obj in objects:
        for geometry in obj.geometry:
            written_verts += geometry.to_obj(output_file, written_verts)
    return written_verts

