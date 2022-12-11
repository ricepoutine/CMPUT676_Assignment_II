from math import log
import solvers
from helper import get_values, avg
from data import data_generator
from os import makedirs
import numpy as np


def main():
    N = 100000 #number of items total
    M = 5 #number of experiments
    #only need weight_max (for inf case), pmin, pmax
    pmin_list = [10]
    pmax_list = [1000]
    w_max_list = [0.1, 0.01, 0.001]

    for x, w in enumerate(pmin_list):
        offline = []
        online = []
        ratio = []
        opts = []
        algs = []
        opts_var = []
        algs_var = []
        w_max = w_max_list[x]
        pmin = pmin_list[0]
        pmax = pmax_list[0]
        # experimental trials for given pmin, pmax, wmax, and N
        for s in range(M):
            OnlineKnapsack = solvers.ThresholdKnapsack(pmin, pmax)
            print(f"building world: {s}")
            items = data_generator(N, w_max, pmin, pmax, s)
            print(f"world build complete")
            print(f"adding items to knapsack")
            for i in range(len(items)):
                OnlineKnapsack.add_item(items[i])
            optimal_solver = solvers.LP_knapsack(items)
            offline_total = get_values(items, optimal_solver)
            online_total = get_values(items, OnlineKnapsack.decisions)
            print(offline_total, online_total)
            opts.append(offline_total[0])
            algs.append(online_total[0])
        empirical_ratio = avg(opts)/avg(algs)
        opts_var.append(np.var(opts))
        algs_var.append(np.var(algs))
        offline.append(avg(opts))
        online.append(avg(algs))
        ratio.append(empirical_ratio)
        theoretical_ratio = 1+log((pmax/pmin))
        print("alpha: " + str(empirical_ratio), "alpha_theoretic >= ", theoretical_ratio)

        file_name = f'pmin{pmin}'
        makedirs('output', exist_ok=True)
        with open(f'output/{file_name}.csv', 'w') as f:
            f.write('offline,online,ratio,opt_var, alg_var\n')
            for i in range(len(online)):
                f.write(f'{offline[i]},{online[i]},{ratio[i]},{opts_var[i]},{algs_var[i]}')

if __name__ == "__main__":
    main()