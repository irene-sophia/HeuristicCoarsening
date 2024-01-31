def delete_end_nodes(links, weights, nodes, exempt_ids):
    all_nodes = [node for node in nodes if node.neighbor_length == 1]
    if exempt_ids:
        indexes = [nodes.index(node) for node in nodes if node.id in exempt_ids]
        all_nodes = [node for i, node in enumerate(all_nodes) if i not in indexes]
    all_link_ids = [node.predecessors + node.successors for node in all_nodes]
    index = [i for i, link in enumerate(links) if link.id in all_link_ids]
    links = [link for i, link in enumerate(links) if i not in index]
    weights = [weight for i, weight in enumerate(weights) if i not in index]
    return links, weights