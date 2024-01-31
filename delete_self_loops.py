from delete_duplicate_edges import delete_duplicate_edges


def delete_self_loops(links, weights, exempt_ids):
    o_nodes = [link['o_node'] for link in links]
    d_nodes = [link['d_node'] for link in links]
    
    if not exempt_ids:
        indexes = [i for i, (o, d) in enumerate(zip(o_nodes, d_nodes)) if o != d]
        links = [links[i] for i in indexes]
        weights = [weights[i] for i in indexes]
    else:
        indexes = [i for i, (o, d) in enumerate(zip(o_nodes, d_nodes)) if o == d]
        indexo = [o in exempt_ids for o in o_nodes[indexes]]
        indexd = [d in exempt_ids for d in d_nodes[indexes]]
        c = [i or j for i, j in zip(indexo, indexd)]
        d = [i for i, j in zip(indexes, c) if not j]
        links = [links[i] for i in d]
        weights = [weights[i] for i in d]
    
    links, weights = delete_duplicate_edges(links, weights)
    
    return links, weights
