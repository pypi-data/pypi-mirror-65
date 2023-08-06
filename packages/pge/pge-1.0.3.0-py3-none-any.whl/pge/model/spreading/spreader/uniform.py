import numpy as np
from random import choice

from pge.model.spreading.spreader.basic import SpreadingModel


class UniformGossip(SpreadingModel):
    def iteration(self):
        node = choice(self.graph.get_ids(stable=True))

        if self.graph.directed():
            others = self.graph.get_in_degrees(node)
        else:
            others = self.graph.get_degrees(node)
        u = others[np.random.randint(0, others.size, 1)][0]
        nws = list(np.unique(self.status[u] + self.status[node]))
        self.status.update({node: nws})
