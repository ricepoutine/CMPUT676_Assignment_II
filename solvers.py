from pulp import LpProblem, LpVariable, PULP_CBC_CMD, LpMaximize, LpBinary, lpSum
import numpy as np

class ThresholdKnapsack(object):
    def __init__(self, pmin, pmax):
        self.pmin = pmin
        self.pmax = pmax
        self.beta = 1/(1+np.log(self.pmax/self.pmin))
        self.decisions = []
        self.y = 0

    def threshold(self, weight):
        if self.y + weight < self.beta:
            return self.pmin
        else:
            return self.pmin*np.exp((self.y+weight)/self.beta-1)

    def add_item(self, item):
        x = 1
        threshold_value = self.threshold(item.weight)
        if item.cost < threshold_value:
            x = 0
        if x == 1:
            self.y += item.weight
        self.decisions.append(x)


def LP_knapsack(items):
    problem = LpProblem('LP_Knapsack', LpMaximize)
    values = []
    weights = []
    for i, item in enumerate(items):
        x = LpVariable(f'x_{i:09d}', cat=LpBinary)
        values.append(x * item.value)
        weights.append(x * item.weight)
    problem += (lpSum(weights) <= 1) #constraint on weight
    problem += lpSum(values) #max problem
    problem.solve(solver=PULP_CBC_CMD(msg=False))
    choices = []
    for variable in problem.variables():
        choices.append(variable.value()) #array of x's
    return choices

def greedy_solver(total):
    value = 0
    capacity = 0
    sortedTotal = sorted(total, key=lambda x: x.cost, reverse=True)
    for item in sortedTotal:
        if (capacity + item.weight) < 1: 
            value += item.cost
            capacity += item.weight
    return value, capacity
