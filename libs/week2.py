from typing import Optional
from itertools import chain, combinations
import numpy as np

import week1


def generate_data_points(matrix: np.ndarray, num: int = 1000):
    if matrix.shape[0] != 2:
        raise ValueError("Expected exactly two rows")

    # Probability of playing action 1
    x = np.linspace(0, 1, num)
    y = np.array([week1.best_response_value_row(matrix, np.array([i, 1 - i])) for i in x])

    return [x, y]


def support_with_values_to_full_strategy(size: int, support_col: list[int], values: np.ndarray):
    strategy = np.zeros(size)
    np.put(strategy, support_col, values)
    return strategy


def verify_support_one_side_with_value(matrix: np.ndarray, support_row: list[int], support_col: list[int]) -> Optional[tuple[np.ndarray, float]]:
    """
    Tries to see whether the column player can mix their strategies in the support so that the values of the row player
    are best-responding
    """

    matrix = matrix[np.ix_(support_row, support_col)]  # select only support

    A_eq = np.concatenate([matrix, -np.ones((matrix.shape[0], 1))], axis=1) # all rows needs to add to th same value
    A_eq = np.concatenate([A_eq, np.array([[1] * matrix.shape[1] + [0]])], axis=0) # probabilities needs to add to one
    
    b_eq = np.array([[0] * matrix.shape[0] + [1]]).transpose()

    try:
        # There may be a solution where the column player would choose a strategy which support is a proper subset of
        # the support_col, which is not what we want. We want the support_col, to be the support of the mixed strategy
        # of the column player
        solution = np.linalg.solve(A_eq, b_eq)
        probabilities = solution[:-1, 0]
        value = solution[-1, 0]

        if not np.isclose(np.zeros(probabilities.shape), probabilities).any():
            return probabilities, value

        return None
    except np.linalg.LinAlgError:
        return None

def verify_support_one_side(matrix: np.ndarray, support_row: list[int], support_col: list[int]) -> Optional[np.ndarray]:
    result = verify_support_one_side_with_value(matrix, support_row, support_col)
    
    if result is None:
        return None
    
    return result[0]

def powerset(iterable, size_start=0):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(size_start, len(s) + 1))


def get_nash_equilibria(row_player_utility: np.ndarray, col_player_utility: np.ndarray):
    assert row_player_utility.shape == col_player_utility.shape

    actions_row = list(range(row_player_utility.shape[0]))
    actions_column = list(range(row_player_utility.shape[1]))    

    for support_row in powerset(actions_row, 1):
        for support_col in powerset(actions_column, 1):
            col_strategy_ = verify_support_one_side_with_value(row_player_utility, support_row, support_col)
            row_strategy_ = verify_support_one_side_with_value(col_player_utility.T, support_col, support_row)

            if col_strategy_ is not None and row_strategy_ is not None:
                col_strategy, col_value = col_strategy_
                row_strategy, row_value = row_strategy_

                col_strategy = support_with_values_to_full_strategy(len(actions_column), support_col, col_strategy)
                row_strategy = support_with_values_to_full_strategy(len(actions_row), support_row, row_strategy)

                row_utility = row_player_utility @ col_strategy
                row_max_utility = np.max(row_utility)

                if not np.isclose(row_max_utility, col_value):
                    continue
                
                column_utility = row_strategy.T @ col_player_utility
                col_max_utility = np.max(column_utility)
                
                if not np.isclose(col_max_utility, row_value):
                    continue
                
                yield (row_strategy, col_strategy)
