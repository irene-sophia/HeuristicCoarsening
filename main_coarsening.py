# create the coarsened links and nodes from the link table and node table 
# created from shape files. The network of Amsterdam is saved in folder as
# network-reduction.mat. You can create your own network in 
# main_create_network.py script file

# Coarsening Function
# new_links, new_vertex, new_weights = coarsening(links, vertex, weights, exempt_ids, pruning, threshold, iterations, constraint_links, flag_intersection)
# Parameters
# flag_study_area   - default is 0; 0 if you need to coarsen the whole   
#                     area (exempt_ids is empty), 1 for the study area 
#                     application where all nodes in the study area  
#                     (defined in exempt_ids) are preserved. 
# flag_intersection - default is 0; 0 if you want to coarsen all nodes, 
#                     1 for the intersection application where all nodes  
#                     other than the intersections are collapsed.
# constraint_links  - default is 1; 0 if you need to reduce the number of 
#                     nodes, 1 if you need to reduce the number of links
# pruning           - default is 0; 0 for pruning disabled, 1 for pruning enabled
# threshold         - 0 is the minimum threshold, maximum is variance(1,36)
#                     in case of using road type as the weights
# iterations        - 1 is the minimum threshold, set a high value for 
#                     maximum iterations. The iterations will be stopped 
#                     automatically when it converges.

import numpy as np
import networkx as nx
import osmnx as ox
import pickle

from shapely.wkt import loads

from coarsening import coarsening
from plot_network import plot_network
from define_study_area import define_study_area
from main_create_network import city_graph
from cut_graph_to_boundaries import cut_graph


# load network or create network
# main_create_network                                                       # <- uncomment to create Amsterdam network and then load network
# load('network.mat')

# for city in ['Utrecht', 'Manhattan', 'Winterswijk']:
for city in ['Winterswijk']:
    for pruning in [0, 1]:
        for iterations in [1, 1000]:
            for threshold in [0, 1000]:

                G, _, _ = city_graph(city, 0)
                G = cut_graph(G, city)
                print(city, pruning, iterations, threshold, 'number of nodes original graph: ', len(G.nodes()))
                num_neighbors = {i: len(G.adj[i]) for i in G.nodes()}
                nx.set_node_attributes(G, num_neighbors, 'num_neighboring_nodes')
                # links = G.edges(data=True)
                # vertex = G.nodes(data=True)
                links = {(u,v): data for u,v,data in G.edges(data=True)}
                for id, link in enumerate(links):
                    links[link]['id'] = id
                vertex = {u: data for u,data in G.nodes(data=True)}


                # initialize weights. Here the weights are the road type
                # types = []
                # for (u, v), data in links.items():
                #     if type(data['highway']) == list:
                #         types.append(data['highway'][0])
                #     else:
                #         types.append(data['highway'])
                #
                # # weight dict
                # weight_dict = {'motorway': 1,
                #                'trunk': 2,
                #                'primary': 3,
                #                'secondary': 4,
                #                'tertiary': 5,
                #                'unclassified': 6,
                #                'residential': 7,
                #                'service': 8,
                #                'motorway_link': 9,
                #                'trunk_link': 10,
                #                'primary_link': 11,
                #                'secondary_link': 12,
                #                'tertiary_link': 13,
                #                'living_street': 14,
                #                'pedestrian': 15,
                #                'track': 16,
                #                'bus_guideway': 17,
                #                'raceway': 18,
                #                'road': 19,
                #                'busway': 20,
                #                'footway': 21,
                #                'bridleway': 22,
                #                'steps': 23,
                #                'path': 24,
                #                'cycleway': 25,
                #                'proposed': 26,
                #                'construction': 27,
                #                'bus_stop': 28,
                #                'crossing': 29,
                #                'elevator': 30,
                #                'emergency_access_point': 31,
                #                'escape': 32,
                #                'give_way': 33,
                #                'mini_roundabout': 34,
                #                'motorway_junction': 35,
                #                'passing_place': 36,
                #                'rest_area': 37
                #                }
                #
                # #retrieve weights on road type
                # weights = {i: (1/weight_dict[x]) for i, x in enumerate(types)}
                # for id, link in enumerate(links):
                #     links[link]['weight'] = weights[id]

                # weights: betweenness centrality
                betweenness_centralities = nx.edge_betweenness_centrality(G, normalized=True, weight='travel_time')
                with open(f"networks/betweenness_centrality_{city}.pkl", 'wb') as f:
                    pickle.dump(betweenness_centralities, f)
                betweenness_centralities = list(betweenness_centralities.values())
                print(min(betweenness_centralities))
                print(max(betweenness_centralities))

                # betweenness_centralities = list(betweenness_centralities.values())
                #
                # weights = {i: (1/weight_dict[x]) for i, x in enumerate(betweenness_centralities)}
                # for id, link in enumerate(links):
                #     links[link]['weight'] = weights[id]
                #
                # with open(f'networks/escape_nodes_{city}.pkl', 'rb') as f:
                #     escape_nodes = pickle.load(f)
                # with open(f'networks/fugitive_start_{city}.pkl', 'rb') as f:
                #     fugitive_start = pickle.load(f)
                # with open(f'networks/start_police_{city}.pkl', 'rb') as f:
                #     police_start = pickle.load(f)
                #
                # # initialize the parameters
                # # exempt ids could be exit nodes, fug start, pol start
                # params = {
                #     'flag_study_area': 0,
                #     'flag_intersection': 0,
                #     'exempt_ids': escape_nodes + [fugitive_start] + police_start,
                #     # 'exempt_ids': [],
                #     'pruning': pruning,
                #     'threshold': threshold,
                #     'iterations': iterations,
                #     'constraint_links': 1
                # }
                #
                # # if params['flag_study_area'] == 1:
                # #     # load('study_area_boundary.mat')                                        # sample study area boundary of amsterdam
                # #     params['exempt_ids'] = define_study_area(vertex, lat_min, lat_max, lon_min, lon_max)
                #
                # # coarsening framework
                # new_links, new_vertex, new_weights = coarsening(links, vertex, weights, params)
                #
                # # reconstruct G from links & nodes:
                # # G_from_links = nx.from_edgelist(new_links)  # when links = G.edges(data=True)
                # # datas = {}
                # # for v, data in G.nodes(data=True):  # G: old graph
                # #     datas[v] = data
                # # nx.set_node_attributes(G_from_links, datas)
                #
                # # G_from_links = nx.DiGraph(new_links)
                #
                # for link in new_links:
                #     if 'geometry' in new_links[link].keys():
                #         if type(new_links[link]['geometry']) == str:
                #             new_links[link]['geometry'] = loads(new_links[link]['geometry'])
                #
                # new_links_mdg = {}
                # for (u, v), data in new_links.items():
                #     new_links_mdg[u, v, 0] = data
                #
                # G_from_links = nx.from_edgelist(new_links, create_using=nx.MultiDiGraph)
                # nx.set_edge_attributes(G_from_links, new_links_mdg)
                # nx.set_node_attributes(G_from_links, new_vertex)
                #
                # # Save results
                # # np.savez('network-reduction.npz', new_links=new_links, new_vertex=new_vertex, new_weights=new_weights)
                # # with open(f"results/coarsened_network_{city}_pruning{pruning}_iter{iterations}.pkl", 'wb') as f:
                # #     pickle.dump(G_from_links, f)
                # print('number of nodes before adding detailed areas: ', len(G_from_links.nodes()))
                # G, _, _ = city_graph(city, 0)
                #
                # # add detailed graph around start locs
                # cf = '["highway"~"motorway|motorway_link|trunk|trunk_link|primary|secondary|tertiary|residential"]'
                # if city == 'Amsterdam':
                #     cf = '["highway"~"motorway|motorway_link|trunk|trunk_link|primary|secondary"]'
                #
                # x = nx.get_node_attributes(G, "x")
                # y = nx.get_node_attributes(G, "y")
                # detailed_graphs = []
                # for node in police_start + [fugitive_start] + escape_nodes:
                #     if city == 'Winterswijk' and node in escape_nodes:
                #         G_node = ox.graph.graph_from_point((y[node], x[node]), dist=2000, custom_filter=cf)
                #     # if city == 'Amsterdam' and node == 2362166488:
                #     #     G_node = ox.graph.graph_from_point((y[node], x[node]), dist=3000, custom_filter=cf)
                #     else:
                #         try:
                #             G_node = ox.graph.graph_from_point((y[node],x[node]), dist=500, custom_filter=cf)
                #             # print('yes', node)
                #         except:
                #             # print(node, 'cannot be used to construct a graph')
                #             pass
                #
                #     detailed_graphs.append(G_node)
                #
                # G_comb_coarsened = nx.compose_all([G_from_links]+detailed_graphs)
                # G_comb_orig = nx.compose_all([G]+detailed_graphs)
                # if city not in ['Utrecht', 'Rotterdam']:
                #     assert set(police_start + [fugitive_start] + escape_nodes).issubset(G_comb_coarsened.nodes())
                #
                # # cut to boundaries (function)
                # if city != 'Amsterdam':
                #     G_comb_coarsened = cut_graph(G_comb_coarsened, city)
                #     G_comb_orig = cut_graph(G_comb_orig, city)
                #
                # print('number of nodes after adding detailed areas: ', len(G_comb_coarsened.nodes()))
                #
                # with open(f"networks/coarsened_network_{city}_pruning{pruning}_iter{iterations}_threshold{threshold}.pkl", 'wb') as f:
                #     pickle.dump(G_comb_coarsened, f)
                #
                # ox.save_graphml(G_comb_coarsened, f"networks/coarsened_network_{city}_pruning{pruning}_iter{iterations}_threshold{threshold}.graph.graphml")
                #
                # # # Visualise the results
                # plot_network(G_comb_coarsened, G, city, pruning, iterations, threshold)
                # # figure; plot_network(new_links, new_vertex)