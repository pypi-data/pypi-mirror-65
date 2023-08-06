import numpy as np
import networkx as nx


def bellman_ford_distance(weights):
    """
    https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm
    """

    n = weights.shape[0]

    # Step 1: initialize graph
    distance = np.empty((n,n))
    distance.fill(np.Inf)
    np.fill_diagonal(distance, 0)

    # Step 2: relax edges repeatedly
    for _ in np.arange(1, n):
        for (u, v), w in np.ndenumerate(weights):
            if w == 0:
                continue

            distance[v] = np.where(distance[v] > distance[u]+w, distance[u]+w, distance[v])

    return distance


def information_centrality(graph):
    return nx.information_centrality(graph.get_nx_graph())


def closeness_centrality(graph):
    return nx.closeness_centrality(graph.get_nx_graph())
