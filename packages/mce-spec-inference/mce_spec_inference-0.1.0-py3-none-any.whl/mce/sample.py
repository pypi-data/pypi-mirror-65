from typing import Sequence

import funcy as fn
import numpy as np
from bdd2dfa.b2d import BNode
from scipy.special import logsumexp

from mce.policy3 import BitPolicy


def coin_flips(n) -> Sequence[bool]:
    return 


def sample(ctrl):
    node = ctrl.root
    while node != "DUMMY":
        kids = ctrl.graph.neighbors(node)
        probs = [ctrl.prob(node, k) for k in kids]
        node2 = np.random.choice(kids, p=probs)

        delta = graph.nodes[node2]['lvl'] - graph.nodes[node]['lvl']
        if ctrl.graph.nodes[node]['decision']:
            delta -= 1  # Use one bit
            yield ctrl.graph.edges[(node, node2)]['action']

        yield from coin_flips(delta)
        node = node2
