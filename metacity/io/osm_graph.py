from metacity.geometry import Graph, Node, Edge, Progress
from metacity.utils.filesystem import read_json
from metacity.io.geojson import Feature, parse_geometry



def iparse_edges(edge_file: str, from_crs: str, to_crs: str):
    edges = read_json(edge_file)

    for f in edges['features']:
        feature = Feature(f)
        if feature.geometry.geometry_type not in ['linestring', 'multilinestring']:
            print(f"Skipping non-linestring feature while parsing graph edges: {feature.geometry.geometry_type}")
            continue

        attr_list = parse_geometry(feature, from_crs, to_crs)
        attr = attr_list[0] # assume linestring has only one attribute
        yield attr, feature.properties


def iparse_nodes(node_file: str, from_crs: str, to_crs: str):
    nodes = read_json(node_file)
    for f in nodes['features']:
        feature = Feature(f)
        if feature.geometry.geometry_type != 'point':
            print(f"Skipping non-point feature while parsing graph nodes: {feature.geometry.geometry_type}")
            continue
        
        x, y = feature.geometry.coordinates
        yield x, y, feature.properties  


def parse_edges(edge_file: str, graph: Graph, from_crs: str, to_crs: str):
    edges_load = Progress(f"Loading edges")
    for i, (attr, props) in enumerate(iparse_edges(edge_file, from_crs, to_crs)):
        edges_load.update()
        u, v = props['u'], props['v']
        edge = Edge(i, u, v, attr, props)
        graph.add_edge(edge)


def parse_nodes(node_file: str, graph: Graph, from_crs: str, to_crs: str):
    nodes_load = Progress(f"Loading nodes")
    for x, y, props in iparse_nodes(node_file, from_crs, to_crs):
        nodes_load.update()
        node = Node(props['id'], x, y, props)
        graph.add_node(node)


def parse_graph(node_file: str, edge_file: str, from_crs: str = None, to_crs: str = None):
    graph = Graph()
    parse_nodes(node_file, graph, from_crs, to_crs)
    parse_edges(edge_file, graph, from_crs, to_crs)
    return graph


        
        
        



