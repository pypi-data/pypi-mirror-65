import numpy as np

from pge.wlk.walker import RandomWalk


class RandomNeighbourNode(RandomWalk):
    def generate(self, n, st=None):
        if st is None:
            st = np.random.choice(self.gr.get_ids())
        res = [st]

        for _ in np.arange(1, n):
            if self.gr.count_out_degree(res[-1]) == 0:
                res.append(res[0])
            else:
                res.append(np.random.choice(self.gr.get_out_degrees(res[-1])))
        return np.array(res)
