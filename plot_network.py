import networkx as nx
import matplotlib.pyplot as plt
import osmnx as ox

def node_colors(G):
    node_size = []
    node_color = []
    for node in G.nodes:
        # if node == suspect_start:
        #     node_size.append(40)
        #     node_color.append('tab:orange')
        # elif node in exit_nodes:
        #     node_size.append(40)
        #     node_color.append('tab:red')
        # elif node in trunk_nodes:
        #     node_size.append(40)
        #     node_color.append('tab:red')
        # else:
        #     node_size.append(0)
        #     node_color.append('lightgray')
        node_size.append(10)
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

def plot_network(G_coarsened, G_orig):
    #TODO: do not make a new graph here but instead work with the same G throughout

    mdg = nx.MultiDiGraph(incoming_graph_data=G_coarsened)
    mdg.graph['crs'] = 4326

    node_size, node_color = node_colors(G_orig)
    edge_size, edge_color = edge_colors(G_orig)
    fig = ox.plot_graph(G_orig, 
                        bgcolor="white", node_color=node_color, node_size=node_size, 
                        edge_linewidth=edge_size, edge_color=edge_color,
                        show=False, save=True, filepath='Rotterdam_orig.png')

    node_size, node_color = node_colors(G_coarsened)
    edge_size, edge_color = edge_colors(G_coarsened)
    fig = ox.plot_graph(mdg, 
                        bgcolor="white", node_color=node_color, node_size=node_size, 
                        edge_linewidth=edge_size, edge_color=edge_color,
                        show=False, save=True, filepath='Rotterdam_coarsened.png')