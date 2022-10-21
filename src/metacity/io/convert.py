from metacity.io.geobuf import encode, decode
from metacity.utils.filesystem import read_json, read_pbf


def json_to_pbf(geojson_file, output_file: str):
    """
    Convert a SHP file to a PBF file.
    """
    data = read_json(geojson_file)
    with open(output_file, 'wb') as f:
        f.write(encode(data))


def pbf_to_json(pbf_file: str):
    """
    Convert a SHP file to a PBF file.
    """
    data = read_pbf(pbf_file)
    return decode(data)

