import numpy as np

class Item(object):
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        self.cost = value/weight

def data_generator(N, w_max, pmin, pmax, seed = 1):
    items = []
    generator = np.random.RandomState(seed)
    for _ in range(N):
        value = generator.rand() #uniform [0,1]
        # weight is either value/pmax, or min(w_max, value/pmin)
        w_u = min(w_max,value/pmin)
        w_l = value/pmax
        weight = generator.rand() * (w_u - w_l) + w_l #enforce uniform distribution
        assert weight < w_u
        assert weight > w_l
        items.append(Item(value, weight))
    return items