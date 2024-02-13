import numpy as np

rock_paper_scissors = np.array([
    [0, 1, -1],
    [-1, 0, 1],
    [1, -1, 0]
])

chicken_a = np.array([
    [0, -1],
    [1, -10]
])

chicken_b = np.array([
    [0, 1],
    [-1, -10]
])

battle_of_sexes_a = np.array([
    [10, 0],
    [0, 7]
])

battle_of_sexes_b = np.array([
    [7, 0],
    [0, 10]
])

# wiki https://en.wikipedia.org/wiki/Strategic_dominance
dominance_example_1_a = np.array([
    [10, 5, 3],
    [0, 4, 6],
    [2, 3, 2]
])

dominance_example_1_b = np.array([
    [4, 3, 2],
    [1, 6, 0],
    [1, 5, 8],
])

# weakly
dominance_example_2_a = np.array([
    [10, 5],
    [0, 4],
])

dominance_example_2_b = np.array([
    [4, 4],
    [1, 6],
])

dominance_example_mixed_1_a = np.array([
    [3, -1],
    [0, 0],
    [-1, 2],
])

dominance_example_mixed_1_b = np.array([
    [-1, 1],
    [0, 0],
    [0, -1],
])

dominance_example_mixed_2_a = np.array([
    [5, 0, 1],
    [3, 0, 3],
    [3, 4, 2]
])

dominance_example_mixed_2_b = np.array([
    [1, 4, 0],
    [1, 0, 5],
    [3, 4, 5]
])