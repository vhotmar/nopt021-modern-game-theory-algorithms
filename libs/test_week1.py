import week1 as week1
import numpy as np
import pytest
from test_utils import rock_paper_scissors

def test_week1_strategy_evaluation():
    matrix = rock_paper_scissors
    row_strategy = np.array([[0.1, 0.2, 0.7]])
    column_strategy = np.array([[0.3, 0.2, 0.5]])

    row_value = week1.evaluate(matrix=matrix, row_strategy=row_strategy, column_strategy=column_strategy)
    assert row_value == pytest.approx(0.08)

def test_week1_best_response_value_calculation():
    matrix = rock_paper_scissors
    row_strategy = np.array([[0.1, 0.2, 0.7]])
    column_strategy = np.array([[0.3, 0.2, 0.5]])
    
    print(row_strategy.shape, column_strategy.shape)

    br_value_row = week1.best_response_value_row(matrix=matrix, row_strategy=row_strategy)
    br_value_column = week1.best_response_value_column(matrix=matrix, column_strategy=column_strategy)
    assert br_value_row == pytest.approx(-0.6)
    assert br_value_column == pytest.approx(-0.2)

def test_week1_iterated_dominated_matrix():
    matrix = np.array([
        [1, 2, 3],
        [2, 4, 4],
        [3, 3, 4]
    ])

    weakly_dominated_rows = week1.find_weakly_dominated_or_equal_row_actions(matrix)
    weakly_dominated_columns = week1.find_weakly_dominated_or_equal_row_actions(matrix.T)

    assert weakly_dominated_rows == [0]
    assert weakly_dominated_columns == [0, 1]

    # Column player will always play the third column (2 + 1), since it is weakly dominating the other two
    # Row player will always play the second (1) or third row (2)
    assert week1.iterated_dominated_matrix(matrix) == (1, 2)
