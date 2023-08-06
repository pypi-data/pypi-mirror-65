import numpy as np


class SpreadingModel(object):
    def __init__(self, graph):
        self.graph = graph
        self.status = {n: [] for n in self.graph.get_ids()}
        self.initial_status = {}
        self.check = 0

    def set_initial_status(self, configuration):
        self.initial_status = configuration
        self.check = np.unique(list(configuration.values())).size

    def init(self):
        self.status = self.initial_status.copy()

    def iteration_bunch(self, nodes):
        self.init()
        n = 0

        while True:
            self.iteration()
            n += 1
            if self.finish(nodes):
                break
        return n

    def iteration_bunch_complex(self, nodes):
        self.init()
        n = 0
        k = 0
        checked = True

        while True:
            self.iteration()
            n += 1

            if self.finish(nodes) and checked:
                k = n
                checked = False
            if self.finish():
                break
        return k, n

    def finish(self, nodes=None):
        if nodes is None:
            nodes = self.graph.get_ids()

        for node in nodes:
            if len(self.status[node]) < self.check:
                return False
        return True

    def iteration(self):
        return None, True
