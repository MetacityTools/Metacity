from metacity.geometry import Graph, Node, Edge, Progress
from metacity.utils.filesystem import read_json
from metacity.io.geojson import Feature, parse_geometry, Projector



def iparse_edges(edge_file: str, projector: Projector):
    edges = read_json(edge_file)
    for f in edges['features']:
        feature = Feature(f)
        if feature.geometry.geometry_type not in ['linestring', 'multilinestring']:
            print(f"Skipping non-linestring feature while parsing graph edges: {feature.geometry.geometry_type}")
            continue

        # TODO here replace parse_geometry with something more efficient
        # avoid using mesh_pipeline functionalities (Attributes)
        attr_list = parse_geometry(feature, projector)
        attr = attr_list[0] #assume edge has only one attribute
        yield attr, feature.properties


def iparse_nodes(node_file: str, projector: Projector):
    nodes = read_json(node_file)
    for f in nodes['features']:
        feature = Feature(f)
        g = feature.geometry
        if g.geometry_type != 'point':
            print(f"Skipping non-point feature while parsing graph nodes: {g.geometry_type}")
            continue
        
        g.set_projection(projector)
        point = g.project([g.coordinates])
        x, y = point[0]
        yield x, y, feature.properties  


def parse_edges(edge_file: str, graph: Graph, projector: Projector):
    progress = Progress(f"Loading edges")
    for i, (attr, props) in enumerate(iparse_edges(edge_file, projector)):
        progress.update()
        u, v = props['u'], props['v']
        edge = Edge(i, u, v, attr, props)
        graph.add_edge(edge)


def parse_nodes(node_file: str, graph: Graph, projector: Projector):
    progress = Progress(f"Loading nodes")
    for x, y, props in iparse_nodes(node_file, projector):
        progress.update()
        node = Node(props['id'], x, y, props)
        graph.add_node(node)


def parse_graph(node_file: str, edge_file: str, from_crs: str = None, to_crs: str = None):
    """
    Load OSM network data exported to GeoJSON format. The required data can be obtained 
    in a following way:

    >>> from pyrosm import OSM
    >>> data = OSM('data.osm.pbf')
    >>> nodes, edges = data.get_network(nodes=True)
    >>> nodes.to_file("nodes.json", driver="GeoJSON") #node_file
    >>> edges.to_file("edges.json", driver="GeoJSON") #edge_file

    The files "nodes.json" and "edges.json" can be then parsed by this function.

    Args:
        node_file (str): path to the GeoJSON file containing the nodes
        edge_file (str): path to the GeoJSON file containing the edges
        from_crs (str): optional CRS to convert the data from
        to_crs (str): optional CRS to convert the data to
    """
    graph = Graph()
    projector = Projector(from_crs, to_crs)
    parse_nodes(node_file, graph, projector)
    parse_edges(edge_file, graph, projector)
    return graph




        



