from typing import Optional

import numpy as np

def evaluate(matrix: np.ndarray, row_strategy: np.ndarray, column_strategy: np.ndarray) -> float:
    return (row_strategy @ matrix @ column_strategy.T)[0, 0]

def best_response_value_row(matrix: np.ndarray, row_strategy: np.ndarray) -> float:
    return np.min(row_strategy @ matrix)

def best_response_value_column(matrix: np.ndarray, column_strategy: np.ndarray) -> float:
    return -np.max(matrix @ column_strategy.T)

def find_weakly_dominated_or_equal_row_actions(matrix: np.ndarray) -> list[int]:
    weakly_dominated = list()
    
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[0]):
            if i == j:
                continue
            
            if (matrix[j, :] >= matrix[i, :]).all():
                weakly_dominated.append(i)
                break
            
    return weakly_dominated


def iterated_dominated_matrix(matrix: np.ndarray) -> Optional[tuple[int, int]]:
    """
    Returns a new strategy for the row player that iteratively eliminates weakly dominated strategies. This means that
    in the end we will get a nash equilibrium (beware it may not be the only one) or nothing
    """
    rows = list(range(matrix.shape[0]))
    columns = list(range(matrix.shape[1]))

    while True:
        weakly_dominated_rows = find_weakly_dominated_or_equal_row_actions(matrix)

        if len(weakly_dominated_rows) != 0:
            row_to_delete = weakly_dominated_rows[0]
            del rows[row_to_delete]
            matrix = np.delete(matrix, [row_to_delete], axis=0)
            continue
        
        weakly_dominated_columns = find_weakly_dominated_or_equal_row_actions(matrix.T)
        
        if len(weakly_dominated_columns) != 0:
            column_to_delete = weakly_dominated_columns[0]
            del columns[column_to_delete]
            matrix = np.delete(matrix, [column_to_delete], axis=1)
            continue
        
        break

    if len(rows) == 1 and len(columns) == 1:
        return rows[0], columns[0]

    return None
