import networkx as nx
import numpy as np

from pge.ranks.extrem_onl import NodeExInfo


class WayEx(NodeExInfo):
    @staticmethod
    def get_ex(gr, root, frm, t1=True):
        pathes = []
        di = []

        pathes_ = nx.single_source_shortest_path(gr.get_nx_graph(), source=root)
        for node in gr.get_ids():
            if node == root:
                continue

            pathes.append(pathes_[node])
            di.append(len(pathes_[node]))

        xs, lv = gr.get_ln_attrs(frm, pathes)
        return WayEx.estimate(xs, lv, t1), np.max(di), np.sum(di)

    @staticmethod
    def get_exes(gr, root, params):
        pathes = []
        di = []

        pathes_ = nx.single_source_shortest_path(gr.get_nx_graph(), source=root)
        for node in gr.get_ids():
            if node == root:
                continue

            pathes.append(pathes_[node])
            di.append(len(pathes_[node]))

        res = []
        for params_ in params:
            xs, lv = gr.get_ln_attrs(params_[0], pathes)
            ex, q = WayEx.estimate(xs, lv, params_[1])
            res.append((ex, q, params_[2]))
        return res, np.max(di), np.sum(di)

    @staticmethod
    def estimate(xs, lv, t1):
        for u in lv[::-1]:
            ts = np.array([])
            for xs_ in xs:
                if t1:
                    ts_ = np.where(xs_ > u)[0]
                else:
                    ts_ = np.where(xs_ <= u)[0]

                if ts_.size > 1:
                    ts = np.append(ts, np.diff(ts_))
                q = np.sum(lv < u) / lv.size

            if ts.size == 0:
                continue

            if np.max(ts) > 2:
                ex = min([1, 2 * np.sum(ts - 1) ** 2 / (ts.size * np.sum(np.multiply(ts - 1, ts - 2)))])
            else:
                ex = min([1, 2 * np.sum(ts) ** 2 / (ts.size * np.sum(ts ** 2))])
            if ex < 1:
                return ex, q
        return 1, 0

    @staticmethod
    def get_test(gr, root, frm, t1=True):
        pathes = []
        di = []

        pathes_ = nx.single_source_shortest_path(gr.get_nx_graph(), source=root)
        for node in gr.get_ids():
            if node == root:
                continue

            pathes.append(pathes_[node])
            di.append(len(pathes_[node]))

        xs, lv = gr.get_ln_attrs(frm, pathes)
        u = lv[int(0.95*lv.size)]
        ts = np.array([])
        for xs_ in xs:
            if t1:
                ts_ = np.where(xs_ > u)[0]
            else:
                ts_ = np.where(xs_ <= u)[0]

            if ts_.size > 1:
                ts = np.append(ts, np.diff(ts_))
        if ts.size == 0:
            return 0, 0, 0, np.max(lv)
        return np.max(ts), np.mean(ts), np.min(ts), u

    @staticmethod
    def get_ex_comm(gr, nodes, frm, t1=True, part=True):
        if part:
            sub = gr.subfraph(nodes)
        else:
            sub = gr

        cmd = gr.get_attributes(frm)
        lv = np.unique(cmd)
        ids = np.array(sub.get_ids())
        ids = ids[np.isin(ids, nodes)]
        cmd = ids[np.isin(ids, nodes)]

        for u in lv:
            if t1:
                rsn = ids[cmd < u]
            else:
                rsn = ids[cmd >= u]

            ts = np.array([])
            for xs_ in xs:
                if t1:
                    ts_ = np.where(xs_ > u)[0]
                else:
                    ts_ = np.where(xs_ <= u)[0]

                if ts_.size > 1:
                    ts = np.append(ts, np.diff(ts_))
            if ts.size == 0:
                return 0, 0, 0, np.max(lv)
            return np.max(ts), np.mean(ts), np.min(ts), u
