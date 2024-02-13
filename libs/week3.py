import numpy as np

import week1 as week1

def compute_deltas(matrix: np.ndarray, row_strategy: np.ndarray, column_strategy: np.ndarray) -> np.ndarray:
    """Computer how much the players could improve if they were to switch to a best response, given utlity of zero-sum game."""
    ev = week1.evaluate(matrix, row_strategy, column_strategy)

    delta_col = ev - week1.best_response_value_row(matrix, row_strategy)
    delta_row = (-ev) - week1.best_response_value_column(matrix, column_strategy)

    return np.array([delta_row, delta_col])

def compute_delta(matrix: np.ndarray, row_strategy: np.ndarray, column_strategy: np.ndarray) -> float:
    ev = week1.evaluate(matrix, row_strategy, column_strategy)
    
    return np.max(matrix @ column_strategy.T) - ev

def compute_exploitability(matrix_a: np.ndarray, matrix_b: np.ndarray, row_strategy: np.ndarray, column_strategy: np.ndarray) -> float:
    delta_a = compute_delta(matrix_a, row_strategy, column_strategy)
    delta_b = compute_delta(matrix_b.T, column_strategy, row_strategy)

    return (delta_a + delta_b) / 2


def compute_epsilon(matrix_a: np.ndarray, matrix_b: np.ndarray, row_strategy: np.ndarray, column_strategy: np.ndarray) -> float:
    """Computes epsilon as defined for epsilon-Nash equilibrium"""
    delta_a = compute_delta(matrix_a, row_strategy, column_strategy)
    delta_b = compute_delta(matrix_b.T, column_strategy, row_strategy)

    return max(delta_a, delta_b)


def compute_exploitability_zero_sum(matrix: np.ndarray, row_strategy: np.ndarray, column_strategy: np.ndarray) -> float:
    """Compute exploitability for a zero-sum game"""
    return 0.0

def uniform_strategy(n: int):
    return np.ones((1, n)) / n

def basis_vector(n: int, i: int):
    vector = np.zeros((1, n))
    vector[0, i] = 1

    return vector

def best_row_response_strategy_to_column_strategy(matrix: np.ndarray, column_strategy: np.ndarray) -> np.ndarray:
    return basis_vector(matrix.shape[0], np.argmax(matrix @ column_strategy.T, axis=0))

def best_column_response_strategy_to_row_strategy(matrix: np.ndarray, row_strategy: np.ndarray) -> np.ndarray:
    return basis_vector(matrix.shape[1], np.argmin(row_strategy @ matrix, axis=1))

def naive_fictitious_self_play(matrix: np.ndarray, steps: int = 100):
    row_strategy = uniform_strategy(matrix.shape[0])
    column_strategy = uniform_strategy(matrix.shape[1])

    exploitability = []

    for _ in range(steps):
        row_strategy = best_row_response_strategy_to_column_strategy(matrix, column_strategy)
        column_strategy = best_column_response_strategy_to_row_strategy(matrix, row_strategy)

        exploitability.append(compute_exploitability(matrix, -matrix, row_strategy, column_strategy))

    return exploitability, (row_strategy, column_strategy)

def fictitious_self_play(matrix: np.ndarray, steps: int = 100):
    row_strategy = uniform_strategy(matrix.shape[0])
    column_strategy = uniform_strategy(matrix.shape[1])

    best_row_response_counts = np.zeros((1, matrix.shape[0]))
    best_column_response_counts = np.zeros((1, matrix.shape[1]))

    exploitability = []

    for _ in range(steps):
        best_row_response_counts += best_row_response_strategy_to_column_strategy(matrix, column_strategy)
        best_column_response_counts += best_column_response_strategy_to_row_strategy(matrix, row_strategy)

        row_strategy = best_row_response_counts / best_row_response_counts.sum()
        column_strategy = best_column_response_counts / best_column_response_counts.sum()

        exploitability.append(compute_exploitability(matrix, -matrix, row_strategy, column_strategy))

    return exploitability, (column_strategy, row_strategy)
