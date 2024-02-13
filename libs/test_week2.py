import numpy as np
import numpy.testing as nptest

import week2 as week2
from test_utils import rock_paper_scissors

def test_week2_verifying_support():
    matrix_p1 = np.array([[0, 0, -10], [1, -10, -10], [-10, -10, -10]])
    matrix_p2 = np.array([[0, 1, -10], [0, -10, -10], [-10, -10, -10]])

    result = week2.verify_support_one_side(matrix = matrix_p1, support_row=[0, 1], support_col = [0, 1])
    nptest.assert_allclose(result, [0.90909, 0.09090], rtol=1e-3)

    result = week2.verify_support_one_side(matrix = matrix_p2.T, support_row=[0, 1, 2], support_col = [0, 1])
    assert result is None
    
def test_week2_support_enumeration_nash_equilibria():
    assert len(
        list(week2.get_nash_equilibria(
            np.array([
                [1, 1, -1],
                [2, -1, 0],
            ]),
            np.array([
                [1/2, -1, -1/2],
                [-1, 3, 2]
            ])
        ))
    ) == 1

    assert len(list(week2.get_nash_equilibria(rock_paper_scissors, -rock_paper_scissors))) == 1

    matrix_p1 = np.array([[0, 0, -10], [1, -10, -10], [-10, -10, -10]])
    matrix_p2 = np.array([[0, 1, -10], [0, -10, -10], [-10, -10, -10]])

    assert len(list(week2.get_nash_equilibria(matrix_p1, matrix_p2))) == 4