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
from shapely.wkt import loads

from coarsening import coarsening
from plot_network import plot_network
from define_study_area import define_study_area
from main_create_network import city_graph

# load network or create network
# main_create_network                                                       # <- uncomment to create Amsterdam network and then load network
# load('network.mat')

G, _, _ = city_graph("Rotterdam", 2300)
num_neighbors = {i: len(G.adj[i]) for i in G.nodes()}
nx.set_node_attributes(G, num_neighbors, 'num_neighboring_nodes')
# links = G.edges(data=True)
# vertex = G.nodes(data=True)
links = {(u,v): data for u,v,data in G.edges(data=True)}
for id, link in enumerate(links): 
    links[link]['id'] = id
vertex = {u: data for u,data in G.nodes(data=True)}


# initialize weights. Here the weights are the road type
types = []
for (u, v), data in links.items():
    if type(data['highway']) == list:
        types.append(data['highway'][0])
    else:
        types.append(data['highway'])

# weight dict
weight_dict = {'motorway': 1, 
               'trunk': 2, 
               'primary': 3, 
               'secondary': 4, 
               'tertiary': 5, 
               'unclassified': 6, 
               'residential': 7, 
               'service': 8, 
               'motorway_link': 9, 
               'trunk_link': 10, 
               'primary_link': 11, 
               'secondary_link': 12, 
               'tertiary_link': 13, 
               'living_street': 14, 
               'pedestrian': 15, 
               'track': 16, 
               'bus_guideway': 17, 
               'raceway': 18, 
               'road': 19, 
               'busway': 20,
               'footway': 21, 
               'bridleway': 22, 
               'steps': 23, 
               'path': 24, 
               'cycleway': 25, 
               'proposed': 26, 
               'construction': 27, 
               'bus_stop': 28, 
               'crossing': 29, 
               'elevator': 30, 
               'emergency_access_point': 31, 
               'escape': 32, 
               'give_way': 33, 
               'mini_roundabout': 34, 
               'motorway_junction': 35, 
               'passing_place': 36, 
               'rest_area': 37
               }    

#retrieve weights on road type 
weights = {i: (1/weight_dict[x]) for i, x in enumerate(types)}
for id, link in enumerate(links): 
    links[link]['weight'] = weights[id]

# initialize the parameters
# TODO: exempt ids should be exit nodes, fug start, pol start
params = {
    'flag_study_area': 0,
    'flag_intersection': 0,
    'exempt_ids': [],
    'pruning': 1,
    'threshold': 1000,
    'iterations': 20,
    'constraint_links': 1
}

if params['flag_study_area'] == 1:
    # load('study_area_boundary.mat')                                        # sample study area boundary of amsterdam
    params['exempt_ids'] = define_study_area(vertex, lat_min, lat_max, lon_min, lon_max)

# coarsening framework
new_links, new_vertex, new_weights = coarsening(links, vertex, weights, params)

# TODO: reconstruct G from links & nodes:
# G_from_links = nx.from_edgelist(new_links)  # when links = G.edges(data=True)
# datas = {}
# for v, data in G.nodes(data=True):  # G: old graph
#     datas[v] = data
# nx.set_node_attributes(G_from_links, datas)

# G_from_links = nx.DiGraph(new_links)

for link in new_links:
    if 'geometry' in new_links[link].keys():
        if type(new_links[link]['geometry']) == str:
            new_links[link]['geometry'] = loads(new_links[link]['geometry'])

G_from_links = nx.from_edgelist(new_links, create_using=nx.DiGraph)
nx.set_edge_attributes(G_from_links, links)
nx.set_node_attributes(G_from_links, vertex)

# Save results
np.savez('network-reduction.npz', new_links=new_links, new_vertex=new_vertex, new_weights=new_weights)

# # Visualise the results
plot_network(G_from_links, G)
# figure; plot_network(new_links, new_vertex)