def delete_end_nodes(G, links, weights, nodes, exempt_ids):
    all_nodes = {k:v for k, v in nodes.items() if v['num_neighboring_nodes'] == 1}
    if exempt_ids:
        all_nodes = {k:v for k, v in all_nodes.items() if k not in exempt_ids}

    # remove links
    ## find connected links
    for node, node_data in all_nodes.items():
        #put rem nodes & rem links in neighbor
        pred_nodes = list(G.predecessors(node))
        succ_nodes = list(G.successors(node))

        if len(pred_nodes) + len(succ_nodes) == 0:
            #remove node
            nodes = {k:v for k, v in nodes.items() if k != node}
            continue

        assert len(pred_nodes) + len(succ_nodes) == 1

        neighbor = (pred_nodes + succ_nodes)[0]
                
        nodes[neighbor]['removed_nodes'] = nodes[neighbor]['removed_nodes'] + nodes[node]['removed_nodes']
        #remove node
        nodes = {k:v for k, v in nodes.items() if k != node}


        #remove links
        pred = list(G.in_edges(node))
        succ = list(G.out_edges(node))

        links = {k:v for k, v in links.items() if k not in pred + succ}

        G.remove_node(node)
        # rem_link = pred + succ
        # G.remove_edge(rem_link[0][0], rem_link[0][1])
    # weights = [weight for i, weight in enumerate(weights) if i not in index]
    return links, nodes, weights