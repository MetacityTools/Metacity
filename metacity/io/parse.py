from metacity.filesystem import base as fs
#from metacity.io.cityjson.parser import parse as parse_cj
from metacity.io.geojson.parser import parse as parse_gj
from metacity.io.shapefile.parser import parse as parse_shp
from metacity.io.sim.parser import parse as parse_sim


def parse_json(input_file: str):
    #try:
    #    parse_cj(layer, input_file)
    #    return 
    #except Exception as e:
    #    e1 = str(e)
    try:
        return parse_gj(input_file)
    except Exception as e:
        e2 = str(e)
    raise Exception(f"Could not parse {input_file}: \nGeoJSON parser:{e2}")


def parse_shapefile(input_file: str):
    try:
        return parse_shp(input_file)
    except Exception as e:
        raise Exception(f"Could not parse {input_file}: \nSHP parser:{e}")

def parse_simfile(input_file: str):
    try:
        return parse_sim(input_file)
    except Exception as e:
        raise Exception(f"Could not parse {input_file}: \nSIM parser:{e}") 

def parse(input_file: str):
    suffix = fs.get_suffix(input_file)
    if suffix == 'json':
        return parse_json(input_file)
    elif suffix == 'shp':
        return parse_shapefile(input_file)
    elif suffix == 'sim':
        return parse_simfile(input_file)
    return []
