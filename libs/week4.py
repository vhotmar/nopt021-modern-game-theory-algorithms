import numpy as np
from scipy.optimize import linprog

def get_nash_equilibria(game: np.ndarray):
    A = game

    rows = A.shape[0]
    vars = rows + 1

    c = np.zeros((1, vars))
    c[0, -1] = 1

    A_ub = np.concatenate([-A, -np.ones((rows,1))], axis=1)
    b_ub = np.zeros((rows, 1))

    A_eq = np.ones((1, vars))
    A_eq[0, -1] = 0
    b_eq = np.ones((1, 1))

    # we can use the default bounds (0, inf), since probabilities are always positive
    
    return linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)

def get_correlated_equilibria(matrix_a: np.ndarray, matrix_b: np.ndarray, c: np.ndarray):
    assert matrix_a.shape == matrix_b.shape

    rows = matrix_a.shape[0]
    cols = matrix_a.shape[1]
    
    vars = rows * cols
    
    def var(row, col):
        return row + col * rows
    
    eqs = []
    
    for ai in range(rows):
        for aj in range(rows):
            if ai == aj:
                continue

            eq = np.zeros((1, vars))

            for b in range(cols):                
                eq[0, var(ai, b)] = -(matrix_a[ai, b] - matrix_a[aj, b])
                
            eqs.append(eq)
    
    for bi in range(cols):
        for bj in range(cols):
            if bi == bj:
                continue

            eq = np.zeros((1, vars))

            for a in range(rows):
                eq[0, var(a, bi)] = -(matrix_b[a, bi] - matrix_b[a, bj])
                
            eqs.append(eq)
                
    A_ub = np.concatenate(eqs, axis=0)
    b_ub = np.zeros((A_ub.shape[0], 1))
    
    A_eq = np.ones((1, vars))
    b_eq = np.ones((1, 1))
    
    return linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)["x"]