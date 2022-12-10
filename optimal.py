from pulp import LpProblem, LpVariable, PULP_CBC_CMD, LpMaximize, LpBinary, lpSum
from data import Item

def offline_knapsack(items: list[Item]):
    problem = LpProblem('Offline_Knapsack', LpMaximize)
    values = []
    weights = []
    for i, item in enumerate(items):
        x = LpVariable(f'x_{i:09d}', cat=LpBinary)
        values.append(x * item.value)
        weights.append(x * item.weight)
    problem += (lpSum(weights) <= 1) #constraint on weight
    problem += lpSum(values) #max problem
    problem.solve(solver=PULP_CBC_CMD(msg=False)) #add threads = 8 after msg
    objective_value = problem.objective.value() #sum of x*values
    decision_variables = []
    for variable in problem.variables():
        decision_variables.append(variable.value()) #array of x's
    return objective_value, decision_variables

def greedy_solver(total):
    value = 0
    capacity = 0
    sortedTotal = sorted(total, key=lambda x: x.cost, reverse=True)
    for item in sortedTotal:
        if (capacity + item.weight) < 1: 
            value += item.cost
            capacity += item.weight
    return value, capacity
