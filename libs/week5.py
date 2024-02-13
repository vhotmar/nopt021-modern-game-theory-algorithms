import numpy as np

from week3 import basis_vector, compute_exploitability, uniform_strategy

def get_strategy_regret_matching(regrets: np.ndarray):
    regrets_plus = np.maximum(regrets, 0)
    regrets_plus_sum = np.sum(regrets_plus)
    
    if np.isclose(regrets_plus_sum, 0):
        return uniform_strategy(regrets.shape[1])
    
    return regrets_plus / regrets_plus_sum

def get_strategy_best_response(regrets: np.ndarray):
    return basis_vector(regrets.shape[1], np.argmax(regrets, axis=1))

def fictitious_self_play(matrix_a: np.ndarray, matrix_b: np.ndarray, steps: int = 2000, strategy=get_strategy_regret_matching):
    assert matrix_a.shape == matrix_b.shape

    row_actions = matrix_a.shape[0]
    column_actions = matrix_a.shape[1]

    row_strategy = uniform_strategy(row_actions)
    column_strategy = uniform_strategy(column_actions)
    
    row_regret = np.zeros((1, row_actions))
    column_regret = np.zeros((1, column_actions))
    
    row_strategy_sum = np.zeros((1, row_actions))
    column_strategy_sum = np.zeros((1, column_actions))

    exploitability = []
    curr_exploitability = []

    for step in range(steps):
        row_strategy = strategy(row_regret)
        column_strategy = strategy(column_regret)
        
        row_strategy_sum += row_strategy
        column_strategy_sum += column_strategy

        exploitability.append(compute_exploitability(matrix_a, matrix_b, row_strategy_sum / (step + 1), column_strategy_sum / (step + 1)))
        curr_exploitability.append(compute_exploitability(matrix_a, matrix_b, row_strategy, column_strategy))
        
        # Given the 
        possible_row_values = (matrix_a @ column_strategy.T).T
        possible_column_values = (row_strategy @ matrix_b)

        row_values = row_strategy @ possible_row_values.T
        column_values = column_strategy @ possible_column_values.T

        row_regret += possible_row_values - row_values
        column_regret += possible_column_values - column_values

    return exploitability, curr_exploitability, (row_strategy_sum / steps, column_strategy_sum / steps)
        
            
        