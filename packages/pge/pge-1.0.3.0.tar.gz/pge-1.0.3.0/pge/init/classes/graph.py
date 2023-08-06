import pandas as pd
import numpy as np
import networkx as nx


class SGraph:
    def __init__(self, gr):
        self.gr = gr
        self.p = None
        self.pi = None

    def __copy__(self):
        return SGraph(self.gr.copy())

    def directed(self):
        return nx.is_directed(self.get_nx_graph())

    def clean(self):
        self.gr.clear()

    def subgraph(self, nodes):
        return SGraph((self.gr.subgraph(nodes)).copy())

    def get_ids(self, stable=False):
        if stable:
            return list(self.gr.nodes())
        else:
            return self.gr.nodes()

    def set_attr(self, ind, attr, value):
        self.gr.nodes[ind][attr] = convert(value)

    def set_attrs(self, attr, values):
        nx.set_node_attributes(self.gr, name=attr, values=values)

    def get_attr(self, ind, attr):
        if hasattr(ind, "__iter__") and not isinstance(ind, str):
            res = []
            for i in ind:
                try:
                    res.append(self.gr.nodes[i][attr])
                except:
                    res.append(0)
            return np.array(res)

        try:
            return self.gr.nodes[ind][attr]
        except:
            return 0

    def get_node_data(self, ind):
        return self.gr.nodes[ind]

    def add_node(self, id_n):
        self.gr.add_node(id_n)

    def add_nodes(self, ids):
        self.gr.add_nodes_from(ids)

    def del_node(self, id_n):
        self.gr.remove_node(id_n)

    def del_nodes(self, ids):
        self.gr.remove_nodes_from(ids)

    def copy(self):
        return SGraph(self.gr.copy())

    def get_attributes(self, attr, nodes=None):
        if nodes is None:
            nodes = self.gr.nodes()

        res = []
        for x in nodes:
            try:
                res.append(self.gr.nodes[x][attr])
            except:
                res.append(-1)
        return np.array(res)

    def get_attrs_dict(self, attr):
        return nx.get_node_attributes(self.gr, attr)

    def get_nx_graph(self):
        return self.gr

    def get_prob_matrix(self):
        if self.p is None:
            p = nx.to_numpy_matrix(self.gr)
            self.p = np.divide(p, np.sum(p, axis=0))
        return self.p

    def get_stat_dist(self):
        if self.pi is None:
            A = np.subtract(np.transpose(self.get_prob_matrix()),
                        np.diag(np.ones(self.size())))
            A = np.vstack([A, np.ones(self.size())])

            b = np.zeros(self.size() + 1)
            b[-1] = 1

            try:
                self.pi = np.linalg.lstsq(A, b, rcond=None)[0]
            except:
                self.pi = np.ones(self.size())
        return self.pi

    def add_edge(self, u, v):
        self.gr.add_edge(u, v)

    def add_edges(self, edges):
        self.gr.add_edges_from(edges)

    def get_edge_data(self, u, v, frm):
        return self.gr[u][v][frm]

    def set_edge_data(self, u, v, to, value):
        self.gr[u][v][to] = value

    def del_edge(self, u, v):
        self.gr.remove_edge(u, v)

    def del_edges_(self, edges):
        self.gr.remove_edges_from(edges)

    def add_path(self, path):
        self.gr.add_path(path)

    def free_in_nodes(self):
        return np.array([n for n in self.get_ids() if self.count_in_degree(n) < self.get_attr(n, "ind")])

    def size(self):
        return self.gr.number_of_nodes()

    def count_in_degree(self, ind, w=None, inn=None):
        res = self.get_in_degrees(ind, w=w)
        if inn is None:
            return res.size
        else:
            return res[np.isin(res, inn)].size

    def count_out_degree(self, out, w=None, inn=None):
        res = self.get_out_degrees(out, w=w)
        if inn is None:
            return res.size
        else:
            return res[np.isin(res, inn)].size

    def count_degree(self, ind, w=None, inn=None):
        if hasattr(ind, "__iter__") and not isinstance(ind, str):
            res = []
            for ind_ in ind:
                res = np.append(res, self.get_degrees(ind_, w=w))
            res = np.unique(res)
        else:
            res = self.get_degrees(ind, w=w)
        if inn is None:
            return res.size
        else:
            return res[np.isin(res, inn)].size

    def count_edges(self, i, j):
        if i.size > j.size:
            return np.array([x[0] for x in self.gr.in_edges(j) if x[0] in i]).size
        else:
            return np.array([x[1] for x in self.gr.out_edges(i) if x[1] in j]).size

    def get_count_edges(self):
        return self.gr.number_of_edges()

    def get_in_degrees(self, ind, un=True, w=None):
        if self.directed():
            try:
                res = [x[0] for x in self.gr.in_edges(ind) if self.get_edge_data(x[0], x[1], w) > 0]
            except:
                res = [x[0] for x in self.gr.in_edges(ind)]

            if un:
                return np.unique(res)
            else:
                return np.array(res)
        else:
            return self.get_degrees(ind, un=un, w=w)

    def get_out_degrees(self, out, un=True, w=None):
        if self.directed():
            try:
                res = [x[1] for x in self.gr.out_edges(out) if self.get_edge_data(x[0], x[1], w) > 0]
            except:
                res = [x[1] for x in self.gr.out_edges(out)]

            if un:
                return np.unique(res)
            else:
                return np.array(res)
        else:
            return self.get_degrees(out, un=un, w=w)

    def get_degrees(self, ind, un=True, w=None):
        try:
            res = [x[0] for x in self.gr.edges(ind) if
                   self.get_edge_data(x[0], x[1], w) > 0 and x[0] != ind] + [x[1] for x in self.gr.edges(ind) if
                                                                             self.get_edge_data(x[0], x[1], w) > 0 and
                                                                             x[1] != ind]
        except:
            res = [x[0] for x in self.gr.edges(ind) if x[0] != ind] + [x[1] for x in self.gr.edges(ind) if
                                                                       x[1] != ind]

        if un:
            return np.unique(res)
        else:
            return np.array(res)

    def update(self, frm, to, node):
        self.gr.node[node][to] = self.gr.node[node][frm]

    def get_data(self, attrs=None, nodes=None):
        if nodes is None:
            nodes = self.gr.nodes()

        if attrs is None:
            attrs = (self.gr.node[nodes[0]]).keys()

        data = []
        for attr in attrs:
            data.append((attr, []))
        ids = []

        for node in nodes:
            ids.append(node)
            for data_line in data:
                data_line[1].append(self.gr.node[node][data_line[0]])

        df = pd.DataFrame(ids, columns=["id"])
        for data_line in data:
            df[data_line[0]] = pd.Series(data_line[1], index=df.index)

        return df

    def save_attrs(self, path, sep=","):
        data = self.get_data()
        data.to_csv(path, sep=sep, index=False)

    def load_attrs(self, path, st=False):
        data = pd.read_csv(path)
        cols = list(data.columns.values)

        for col in cols:
            if col == "id":
                continue
            print(col)
            if st:
                dt = {str(data["id"][i]): str(data[col][i]) for i in np.arange(len(data[col]))}
            else:
                dt = {str(data["id"][i]): convert(data[col][i]) for i in np.arange(len(data[col]))}
            nx.set_node_attributes(self.gr, values=dt, name=col)

    def estimated(self, ind, frm):
        return self.get_attr(ind, frm) >= 0

    def del_attrs(self, attrs):
        if not hasattr(attrs, '__iter__'):
            attrs = [attrs]

        for n in self.get_ids():
            for attr in attrs:
                del self.gr.nodes[n][attr]

    def get_blk_attrs(self, frm, nodes, typ, part=True):
        xs = np.array([])
        blks = np.array([])

        count = 0
        if typ == "sl" or typ == "sl-ext":
            for j in nodes:
                if self.directed():
                    subs = self.get_in_degrees(j)
                else:
                    subs = self.get_degrees(j)
                if typ == "sl-ext":
                    subs = np.append(j, subs)
                if part:
                    subs = subs[np.isin(subs, nodes)]
                if subs.size == 0:
                    continue
                res = self.get_attributes(frm, subs)
                blks = np.append(blks, count * np.ones(res.size))
                xs = np.append(xs, res)
                count = count + 1

        if typ == "b-sl" or typ == "b-sl-ext":
            for j in nodes:
                subs = self.get_out_degrees(j)
                if typ == "b-sl-ext":
                    subs = np.append(j, subs)
                if part:
                    subs = subs[np.isin(subs, nodes)]
                if subs.size == 0:
                    continue
                res = self.get_attributes(frm, subs)
                blks = np.append(blks, count * np.ones(res.size))
                xs = np.append(xs, res)
                count = count + 1

        if typ == "dj":
            subs = []
            blk = []
            subs_ = np.array([])
            blk_ = []

            for j in nodes:
                sub = self.get_out_degrees(j)

                if sub.size > 1:
                    nad = True
                    for prt in np.arange(len(subs)):
                        if np.sum(np.isin(sub, subs[prt])) > 1:
                            nad = False
                            subs[prt] = np.unique(np.append(subs[prt], sub))
                            blks = np.append(blks, blk[prt])
                            break
                    if nad:
                        subs.append(sub)
                        blk.append(count)
                        blks = np.append(blks, count)
                        count += 1
                else:
                    nex = True
                    for prt in np.arange(subs_.size):
                        if subs_[prt] == sub[0]:
                            nex = False
                            blks = np.append(blks, blk_[prt])
                            break

                    if nex:
                        blks = np.append(blks, count)
                        subs_ = np.append(subs_, sub)
                        blk_.append(count)
                        count += 1
                xs = np.append(xs, self.get_attr(j, frm))
        return xs, blks

    def get_ln_attrs(self, frm, nodes):
        xs = []
        lv = np.array([])

        for node in nodes:
            xs.append(self.get_attributes(frm, node))
            lv = np.append(lv, self.get_attributes(frm, node))
        lv = np.unique(lv, return_counts=False)
        return xs, lv

    def get_t_matrix(self, way):
        res = self.get_matrix()
        if not way:
            res = res.transpose()
        return res / (np.sum(res, axis=0) + np.spacing(0))

    def get_matrix(self):
        return nx.to_numpy_matrix(self.get_nx_graph())

def convert(value):
    try:
        return float(value)
    except:
        return str(value)
