import numpy as np
import networkx as nx

from pge.init.classes.graph import SGraph
from rd_pr.dist import pwrlaw
from pge.init.add import actual
from rd_pr.simple import rand_int


class Creator:
    @staticmethod
    def make_tbt(nm, alpha, beta, sigma, min_r=(1, 1)):
        ind_d = np.around(pwrlaw(alpha, nm, min_r[0], 1))
        out_d = np.around(pwrlaw(beta, nm, min_r[1], 1))

        zv = np.sum(np.subtract(ind_d, out_d))
        k = 1 - min([0.5, 1 - alpha ** -1, 1 - beta ** -1]) / 2
        while np.abs(zv) > nm ** k:
            i_s = np.random.choice(np.arange(nm), int(np.abs(zv)), replace=False)

            for i in i_s:
                if zv < 0:
                    ind_d[i] = ind_d[i] + 1
                else:
                    out_d[i] = out_d[i] + 1
            zv = np.sum(np.subtract(ind_d, out_d))

        gr = SGraph(nx.DiGraph())
        gr.add_nodes(np.arange(nm))

        for i in (np.arange(nm)):
            if ind_d[i] == 0:
                continue
            i_s = np.setdiff1d(np.arange(nm), i)
            np.random.shuffle(i_s)

            for j in i_s:
                if out_d[int(j)] > gr.count_out_degree(j):
                    gr.add_edge(j, i)

        actual(gr, sigma)
        return gr

    @staticmethod
    def create_subgraph(g, start_node, sz):
        un = np.array([start_node])
        nxt = np.copy(un)

        while sz >= un.size:
            print(un.size)
            nxt = np.append(g.get_in_degrees(nxt), g.get_out_degrees(nxt))
            un = np.unique(np.append(un, nxt))
        res = g.subgraph(un[:sz])
        return SGraph(res)

    @staticmethod
    def make_from_data(network, pre="../", nm=None, sigma=None):
        path = pre + "samples/networks/web-"
        if network == "BS":
            path += "BerkStan.txt"
        if network == "S":
            path += "Stanford.txt"
        if network == "G":
            path += "Google.txt"
        else:
            path = network
        gr = nx.read_edgelist(path, create_using=nx.DiGraph())
        print("loaded")

        if nm is None:
            res = SGraph(gr)
        else:
            choiced = np.random.choice(gr.nodes())
            res = Creator.create_subgraph(gr, choiced, nm)

        actual(res, sigma)
        print("attrs added")
        return res

    @staticmethod
    def simple_graph(network, pre="../"):
        path = pre + "pge/samples/networks/web-"
        if network == "BS":
            path += "BerkStan.txt"
        if network == "S":
            path += "Stanford.txt"
        if network == "G":
            path += "Google.txt"
        return SGraph(nx.read_edgelist(path, create_using=nx.DiGraph()))

    @staticmethod
    def fire_forest(p_f, p_r, n, sg=2, fl=True):
        graph = nx.DiGraph()
        graph.add_nodes_from(np.arange(n))
        graph = SGraph(graph)

        for i in np.arange(1, n):
            add_n = np.array([])
            if i - 1 == 0:
                ws = np.array([0])
            else:
                ws = np.array([rand_int(mn=0, mx=i - 1, sz=1)])

            while ws.size > 0:
                n_ws = np.array([])
                for w in ws:
                    x = graph.get_in_degrees(w)
                    sub_x = np.random.geometric(p_f) - 1
                    if sub_x < x.size:
                        x = np.random.choice(x, sub_x, replace=False)

                    if x.size != 0:
                        n_ws = np.append(n_ws, x)

                    y = graph.get_out_degrees(w)
                    sub_y = np.random.geometric(p_r) - 1
                    if sub_y < y.size:
                        y = np.random.choice(y, sub_y, replace=False)

                    if y.size != 0:
                        n_ws = np.append(n_ws, y)

                if n_ws.size != 0:
                    n_ws = np.setdiff1d(n_ws, add_n)

                for nl in ws:
                    graph.add_edge(i, int(nl))
                add_n = np.append(add_n, ws)
                ws = n_ws

        if fl:
            actual(graph, sg)
        return graph

    @staticmethod
    def sparse_fire_forest(p_f, p_r, n, sg=2, pr=0.1, ln=3):
        gr = Creator.fire_forest(p_f, p_r, n, sg, fl=False).copy()

        count = n
        for node in np.random.choice(gr.get_ids(stable=True), int(gr.size() * pr)):
            node2 = np.random.choice(gr.get_in_degrees(node), 1)
            gr.del_edge(int(node2), int(node))

            un = rand_int(1, ln, 1)
            gr.add_path([int(node2)] + [int(count + i) for i in np.arange(un)] + [int(node)])
            count = n + un

        actual(gr, sg)
        return gr

    @staticmethod
    def gnp_random_graph(n, p, sg=2, directed=True):
        res = SGraph(nx.generators.fast_gnp_random_graph(n, p, directed=directed))
        actual(res, sg)
        return res

    @staticmethod
    def geometric(n, dis, clean=True, dim=2):
        res = nx.random_geometric_graph(n, dis, dim=dim)
        sub = max(nx.connected_components(res), key=len)
        res = SGraph(res).subgraph(sub)

        if clean:
            res.del_attrs(["pos"])
        return res

    @staticmethod
    def chunglu(seq):
        res = nx.expected_degree_graph(seq, selfloops=False)
        nodes = sorted(nx.connected_components(res), key=len, reverse=True)[0]
        return SGraph(res).subgraph(nodes)

    @staticmethod
    def power_law(n, sigma):
        inds = np.floor(pwrlaw(sigma, n))
        if np.sum(inds) % 2 == 1:
            inds = np.append(inds, [1])

        res = nx.expected_degree_graph([int(u) for u in inds])
        nodes = sorted(nx.connected_components(res), key=len, reverse=True)[0]
        res.remove_edges_from(nx.selfloop_edges(res))
        return SGraph(res).subgraph(nodes)

    @staticmethod
    def load(path):
        return SGraph(nx.read_graphml(path))

    @staticmethod
    def load_adj(path):
        return SGraph(nx.read_adjlist(path))
