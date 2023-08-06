import numpy as np

from pge.model.spreading.spreader.basic import SpreadingModel


class BroadUniformGossip(SpreadingModel):
    def iteration(self):
        nodes = self.graph.get_ids()
        for node in nodes:
            if self.graph.directed():
                others = self.graph.get_in_degrees(node)
            else:
                others = self.graph.get_degrees(node)
            u = others[np.random.randint(0, others.size, 1)][0]
            nws = list(np.unique(self.status[u] + self.status[node]))
            self.status.update({node: nws})
