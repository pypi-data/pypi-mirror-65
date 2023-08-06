import numpy as np


def clustering(gr):
    trng = 0
    conn = 0

    for node in gr.get_ids():
        ind = gr.get_out_degrees(node)

        conn += ind.size * (ind.size - 1)

        for node_ in ind:
            ind_ = gr.get_out_degrees(node, ex_i=[node, node_])
            trng += (ind_[np.isin(ind_, ind)]).size

    return trng / conn
