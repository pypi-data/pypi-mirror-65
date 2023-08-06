import numpy as np
import networkx as nx

from itertools import combinations


def phi(gr, nodes, other=None):
    if gr.directed():
        ind_i = np.arange(gr.size())[[node in nodes for node in gr.get_ids()]]
        if other is not None:
            ind_j = np.arange(gr.size())[[node in other for node in gr.get_ids()]]
        else:
            ind_j = np.arange(gr.size())[[node not in nodes for node in gr.get_ids()]]
        pi = gr.get_stat_dist()
        c = np.sum(pi[ind_i])
        v = np.sum(pi[ind_j])

        p = gr.get_prob_matrix()
        w = np.multiply(p, pi)

        p1 = np.sum(w[np.ix_(ind_j, ind_i)])
        p2 = np.sum(w[np.ix_(ind_i, ind_j)])
        return np.max([p1 / c, p2 / v])
    else:
        return nx.algorithms.cuts.conductance(gr.get_nx_graph(), nodes, other)


def conductance_set(gr, root):
    nxt = [root]
    prev2 = 3
    prev1 = 2

    while len(nxt) < gr.size():
        ind = gr.get_degrees(nxt)
        ind = ind[~np.isin(ind, nxt)]

        cnd = [phi(gr, nxt + [node]) for node in ind]
        mn = np.argmin(cnd)

        if prev2 >= prev1 and prev1 <= cnd[mn]:
            break

        nxt.append(ind[mn])
        prev2 = prev1
        prev1 = cnd[mn]
    return nxt


def conductance(gr):
    res = []
    res_n = []

    for i in np.arange(1, gr.size()):
        for nodes in list(combinations(gr.get_ids(), i)):
            if not nx.is_connected(gr.subgraph(nodes).get_nx_graph()):
                continue
            res.append(phi(gr, nodes))
            res_n.append(nodes)

    ind = np.argmin(res)
    return res[ind], res_n[ind]


def weak_conductance(gr, c):
    st = {}
    for node in gr.get_ids():
        st.update({node: []})

    for i in np.arange(max([int(gr.size() / c), 2]), int((gr.size() + 1)/2)):
        print(i, "!")

        for nodes in list(combinations(gr.get_ids(), i)):
            rs1 = []
            if nx.number_of_isolates(gr.subgraph(nodes).get_nx_graph()) != 0 and i != 1:
                continue

            for j in np.arange(1, i):
                for nodes_ in list(combinations(nodes, j)):
                    if nx.number_of_isolates(gr.subgraph(nodes_).get_nx_graph()) != 0 and j != 1:
                        continue
                    ph = phi(gr, nodes_, [nd for nd in nodes if nd not in nodes_])
                    rs1.append(ph)

            for node in gr.get_ids():
                if node not in nodes:
                    continue

                ind = np.argmin(rs1)
                st.get(node).append((rs1[ind], nodes))

    res = {}
    for node in gr.get_ids():
        tmp1 = []
        tmp2 = []
        for st_ in st.get(node):
            tmp1.append(st_[0])
            tmp2.append(st_[1])
        ind = np.argmax(tmp1)

        res.update({node: (tmp1[ind], tmp2[ind])})
    return res


def diweak_conductance(gr, node, c):
    tmp1 = []
    tmp2 = []

    nodes = [[node]]
    for i in np.arange(2, int(gr.size()/2)):
        print(i, "!")

        nodes_ = []
        for nds in nodes:
            nexts = gr.get_in_degrees(nds)
            for next in nexts:
                if np.unique([next] + nds).size < i:
                    continue

                nnodes = [next] + nds
                subs = gr.subgraph(nnodes).get_nx_graph()
                if nx.diameter(subs) >= c + 1:
                    continue

                tsubs = nx.algorithms.community.kernighan_lin_bisection(subs)
                tmp1.append(phi(gr, tsubs[0], tsubs[1]))
                tmp2.append(nnodes)
                nodes_.append(nnodes)
        nodes = nodes_

        if len(nodes) == 0:
            break

    if len(tmp1) == 0:
        return 1, [node]
    ind = np.argmax(tmp1)
    return tmp1[ind], tmp2[ind]
