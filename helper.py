import numpy as np

def get_values(items, decisions):
    assert len(items) == len(decisions)
    total_value = np.sum([i.value * x for i,x in zip(items, decisions)], axis=0)
    total_weight = np.sum([np.multiply(i.weight, x) for i, x in zip(items, decisions)], axis=0)
    return total_value, total_weight

def avg(list):
    return sum(list)/len(list)