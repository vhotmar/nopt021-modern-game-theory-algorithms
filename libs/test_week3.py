import week3 as week3
import week5 as week5
import numpy as np
import pytest

from test_utils import rock_paper_scissors, dominance_example_mixed_2_a, dominance_example_mixed_2_b

def test_week3():
    matrix = rock_paper_scissors
    row_strategy = np.array([[0.1, 0.2, 0.7]])
    column_strategy = np.array([[0.3, 0.2, 0.5]])
    
    print(row_strategy.shape, column_strategy.shape)

    delta_row, delta_column = week3.compute_deltas(matrix=matrix, row_strategy=row_strategy,
                                                   column_strategy=column_strategy)
    assert delta_row == pytest.approx(0.12)
    assert delta_column == pytest.approx(0.68)
    
    assert week3.compute_delta(matrix, row_strategy, column_strategy) == pytest.approx(0.12)
    assert week3.compute_delta(-matrix.T, column_strategy, row_strategy) == pytest.approx(0.68)
    
    ma = np.array([[30, -10, 20], [-10, 20, -20]])
    print(week5.fictitious_self_play(ma, -ma, 200, strategy=week5.get_strategy_best_response))
    
    assert False

    #week3.fictitious_self_play(matrix)