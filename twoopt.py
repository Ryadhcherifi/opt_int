import numpy as np
import math
from random import randint
import time
#from main import calculer_cout
def cost(cost_mat, route):
    # print(route)
    return cost_mat[np.roll(route, 1), route].sum()


def cost_change(cost_mat, n1, n2, n3, n4):
    change = cost_mat[n1][n3] + cost_mat[n2][n4] - cost_mat[n1][n2] - cost_mat[n3][n4]

    if (abs(change) < 1e-8):
        return 0
    else:
        return change

def two_opt2(route, cost_mat):
    route = np.array(route)
    time1 = time.time()
    if route[-1] == route[0]:
        best = np.resize(route, np.size(route, 0) - 1)
    else:
        best = route
    dim = len(best)
    improved = True
    while improved:
        improved = False
        for i in range(dim):
            i1 = (i + 1) % dim
            for j in range(i + 1, dim):
                j1 = (j + 1) % dim
                if ((j != i) and (j != i1) and (j != (i - 1) % dim)):
                    if cost_change(cost_mat, best[i], best[((i + 1) % dim)], best[(j)], best[j1]) < 0:
                        if (j1 == 0):
                            best[0:i1] = best[i::-1]
                        else:

                            best[i1:j1] = best[j:i:-1]

                        improved = True
                        #print(improved, calculer_cout(best, cost_mat))


    time2 = time.time()
    cout = cost(cost_mat, best)
    best = np.resize(best, np.size(best, 0) + 1)
    best[np.size(best, 0) - 1] = best[0]
    return cout, list(best), time2 - time1
