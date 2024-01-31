import networkx as nx
import osmnx as ox

def city_graph(city, distance):
    filepath = f"networks/Graph_{city}_{distance}.graph.graphml"

    # graph = nx.read_graphml(path=filepath, node_type=int, edge_key_type=float)
    graph = ox.load_graphml(filepath)

    for u, v in graph.edges():
        for i in graph[u][v]:  # if multiple edges between nodes u and v
            graph[u][v][i]['travel_time'] = float(graph[u][v][i]['travel_time'])

    labels = {}
    labels_inv = {}
    for i, node in enumerate(graph.nodes()):
        labels[node] = i
        labels_inv[i] = node

    return graph, labels, labels_inv

G, _, _ = city_graph("Rotterdam", 600)