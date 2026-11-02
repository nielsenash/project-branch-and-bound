# See additional instructions for these tests in the instructions for the project
from tsp_solve import get_reduced_cost_matrix


def test_reduced_cost_matrix_1():
    initial_edges = [[1, 2, 3], [6, 3, 3], [4, 4, 8]]
    reduced_matrix, cost = get_reduced_cost_matrix(initial_edges)
    assert(cost == 8)
    assert(reduced_matrix == [[0, 1, 2], [3, 0, 0], [0, 0, 4]])


def test_reduced_cost_matrix_2():
    initial_edges = [[float('inf'), float('inf'), float('inf')], [1, 1, 1], [2, 2, 2]]
    reduced_matrix, cost = get_reduced_cost_matrix(initial_edges)
    assert(cost == float('inf'))
    assert(reduced_matrix == [[float('inf'), float('inf'), float('inf')], [0, 0, 0], [0, 0, 0]])


def test_reduced_cost_matrix_3():
    initial_edges = [[float('inf'), 7], [3, float('inf')]]
    reduced_matrix, cost = get_reduced_cost_matrix(initial_edges)
    assert(cost == 10)
    assert(reduced_matrix == [[float('inf'), 0], [0, float('inf')]])


# Add more tests as necessary...
