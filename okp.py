from math import exp, log, isclose
import random, sys
import numpy as np
import optimal

from data import Item

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
        if item.cost < self.phi or self.y + item.weight > 1:
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
    N = 50000 #number of items total //try 10000
    M = 5 #number of experiments

    pmin = 10 #try 10
    pmax = 1000 #try 1000

    w_max = 0.001 #try 0.001

    #only need weight_max (for inf case), pmin, pmax

    total = []
    opts = []
    algs = []

    Knapsack = ThresholdKnapsack(pmin, pmax)

    # experimental trials
    for s in range(1):
        generator = np.random.RandomState(s)
        print(f"building world: {s}")
        # build world
        for i in range(N):
            value = generator.rand() #uniform [0,1]
            # weight is either value/pmax, or min(w_max, value/pmin)
            w_u = min(w_max,value/pmax)
            w_l = value/pmax
            weight = generator.rand() * (w_u - w_l) + w_l
            assert weight <= w_max
            assert weight >= w_l
            item = Item(value, weight)
            total.append(item)
        print(f"world build complete")
        print(f"adding items to knapsack")
        # add items
        for i in range(N):
            Knapsack.add_item(total[i])
        
        # print result
        optimal_solver = optimal.offline_knapsack(total)
        #optimal_solver = optimal.greedy_solver(total)
        print(optimal_solver[0], Knapsack.total_cost())
        opts.append(optimal_solver[0])
        algs.append(Knapsack.total_cost()[0])
        Knapsack.clear(pmin, pmax)
        total = []
    print("alpha: " + str(avg(opts)/avg(algs)), "alpha_theoretic >= ", 1+log((pmax/pmin)))





if __name__ == "__main__":
    main()