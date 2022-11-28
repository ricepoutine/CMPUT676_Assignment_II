from math import exp, log, isclose
import random, sys

class Item(object):
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
        self.cost = value / weight
        self.accept = 0
    
class ThresholdKnapsack(object):
    def __init__(self, pmin, pmax):
        self.pmin = pmin
        self.pmax = pmax
        self.phi = pmin
        self.beta = 1/(1+log((self.pmax/self.pmin)))
        self.knapsack = []
        self.y = 0

    def update_phi(self):
        if (0 <= self.y < self.beta):
            self.phi = self.pmin
        elif (self.beta <= self.y <= 1):
            self.phi = self.pmin*exp(self.y/(self.beta-1))

    def add_item(self, item):
        if item.cost < self.phi:
            item.accept = 0
        else: 
            # hard check, in case of floating point error
            if self.y + item.weight < 1:
                item.accept = 1
        self.y += item.weight*item.accept
        self.update_phi()
        self.knapsack.append(item)
    
    def total_cost(self):
        cost = 0
        capacity = 0
        for item in self.knapsack:
            if item.accept == 1:
                cost += item.cost
                capacity += item.weight
        return cost, capacity
    
    def clear(self, pmin, pmax):
        self.pmin = pmin
        self.pmax = pmax
        self.phi = pmin
        self.beta = 1/(1+log((self.pmax/self.pmin)))
        self.knapsack = []
        self.y = 0

def optimal_value(total):
    value = 0
    capacity = 0
    sortedTotal = sorted(total, key=lambda x: x.cost, reverse=True)
    for item in sortedTotal:
        if (capacity + item.weight) < 1: 
            value += item.cost
            capacity += item.weight
    return value, capacity

def avg(list):
    return sum(list)/len(list)

def main():
    N = 10000000 #number of items total
    M = 10 #number of experiments
    N_trial = 250000 #sequence length
    weight_L = 1e-8 #sys.float_info.min
    weight_H = 1e-5
    value_L = 1e-10
    value_H = 1e-8
    pmin = value_L/weight_H
    pmax = value_H/weight_L

    total = []
    trial_total = []

    opts = []
    algs = []

    Knapsack = ThresholdKnapsack(pmin, pmax)

    # init world
    for _ in range(N):
        value = random.uniform(value_L, value_H)
        weight = random.uniform(weight_L, weight_H)
        if weight == 0:
            print("rounding error, setting weight to e")
            weight = sys.float_info.min
        item = Item(value, weight)
        total.append(item)

    # experimental trials
    for _ in range(M):
        for i in range(N_trial):
            tmp_item = random.choice(total)
            Knapsack.add_item(tmp_item)
            trial_total.append(tmp_item)
        print(optimal_value(trial_total), Knapsack.total_cost())
        opts.append(optimal_value(trial_total)[0])
        algs.append(Knapsack.total_cost()[0])
        Knapsack.clear(pmin, pmax)
        trial_total = []
    print("alpha: " + str(max(opts)/min(algs)), "alpha_theoretic >= ", 1+log((pmax/pmin)))



    



if __name__ == "__main__":
    main()