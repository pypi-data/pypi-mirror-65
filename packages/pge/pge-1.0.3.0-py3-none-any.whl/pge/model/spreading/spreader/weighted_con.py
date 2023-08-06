import numpy as np

from pge.model.spreading.spreader.basic import SpreadingModel


class WeightedGossip(SpreadingModel):
    def __init__(self, graph, attr):
        super().__init__(graph)
        self.attr = attr

    def iteration(self):
        nodes = self.graph.get_ids()
        for node in nodes:
            if self.graph.directed():
                others = self.graph.get_in_degrees(node)
            else:
                others = self.graph.get_degrees(node)
            p = self.graph.get_attributes(self.attr, others)**-1
            p = p/np.sum(p)
            u = np.random.choice(others, 1, p=p)[0]
            self.status.update({node: list(np.unique(self.status[u] + self.status[node]))})
