import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox
import pickle

def node_colors(G, escape_nodes, fugitive_start, police_start):
    node_size = []
    node_color = []
    for node in G.nodes:
        if node == fugitive_start:
            node_size.append(40)
            node_color.append('tab:orange')
        elif node in police_start:
            node_size.append(40)
            node_color.append('tab:blue')
        elif node in escape_nodes:
            node_size.append(40)
            node_color.append('tab:red')
        else:
            node_size.append(0)
            node_color.append('lightgray')
    
    return node_size, node_color

def edge_colors(G):
    edge_color = ['lightgray'] * len(G.edges())
    edge_size = [1] * len(G.edges())
    # for index, edge in enumerate(G.edges()):
    #     if edge in edges_fugitive:
    #         edge_color[index] = 'tab:orange'
    #         edge_size[index] = 2

    return edge_size, edge_color

def plot_network(G_coarsened, G_orig, city, pruning, iterations, threshold):
    mdg = nx.MultiDiGraph(incoming_graph_data=G_coarsened)
    mdg.graph['crs'] = 4326

    with open(f'networks/escape_nodes_{city}.pkl', 'rb') as f:
        escape_nodes = pickle.load(f)
    with open(f'networks/fugitive_start_{city}.pkl', 'rb') as f:
        fugitive_start = pickle.load(f)
    with open(f'networks/start_police_{city}.pkl', 'rb') as f:
        police_start = pickle.load(f)

    node_size, node_color = node_colors(G_orig, escape_nodes, fugitive_start, police_start)
    edge_size, edge_color = edge_colors(G_orig)
    fig = ox.plot_graph(G_orig, 
                        bgcolor="white", node_color=node_color, node_size=node_size, 
                        edge_linewidth=edge_size, edge_color=edge_color,
                        show=False, save=True, filepath=f'figs/networks/{city}_orig.png')

    node_size, node_color = node_colors(G_coarsened, escape_nodes, fugitive_start, police_start)
    edge_size, edge_color = edge_colors(G_coarsened)
    fig = ox.plot_graph(mdg, 
                        bgcolor="white", node_color=node_color, node_size=node_size, 
                        edge_linewidth=edge_size, edge_color=edge_color,
                        show=False, save=True, filepath=f'figs/networks/{city}_coarsened_pruning{pruning}_iterations{iterations}_threshold{threshold}.png')