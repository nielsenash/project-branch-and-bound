import math
import random

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree

PARAMS_FOR_SMART_BRANCH_AND_BOUND_SMART_TEST = {
    "n": 30,
    "euclidean": True,
    "reduction": 0.2,
    "normal": False,
    "seed": 312,
    "timeout": 20,
}


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(
            SolutionStats(
                tour=tour,
                score=cost,
                time=timer.time(),
                max_queue_size=1,
                n_nodes_expanded=n_nodes_expanded,
                n_nodes_pruned=n_nodes_pruned,
                n_leaves_covered=cut_tree.n_leaves_cut(),
                fraction_leaves_covered=cut_tree.fraction_leaves_covered(),
            )
        )

    if not stats:
        return [
            SolutionStats(
                [],
                math.inf,
                timer.time(),
                1,
                n_nodes_expanded,
                n_nodes_pruned,
                cut_tree.n_leaves_cut(),
                cut_tree.fraction_leaves_covered(),
            )
        ]


def block_rows_and_cols(edges: list[list[float]], start: int, end: int, current):
    new_edges = edges.copy()
    for i in range(len(new_edges)):
        new_edges[start][i] = float('inf')
        new_edges[i][end] = float('inf')
    if len(current) < len(edges) - 1:
        first = current[0]
        new_edges[end][first] = float('inf')
    ignore = set(current)
    return get_reduced_cost_matrix(new_edges, ignore)


def get_reduced_cost_matrix(edges: list[list[float]], ignore=set()):  # overall space / time = O(n^2)
    new_edges = edges.copy()
    cost = 0

    # rows
    for i in range(len(new_edges)):  # time = O(n)
        min_edge = min(new_edges[i])  # time = O(n)
        cost += min_edge
        if min_edge != float('inf'):
            for j in range(len(new_edges[i])):  # time = O(n)
                new_edges[i][j] -= min_edge

    # columns
    for i in range(len(new_edges)):  # time = O(n)
        col_vals = []
        for j in range(len(new_edges)):  # time = O(n)
            col_vals.append(new_edges[j][i])  # space = O(n)
        min_edge = min(col_vals)  # time = O(n)
        cost += min_edge
        if min_edge != float('inf'):
            for k in range(len(new_edges)):  # time = O(n)
                new_edges[k][i] -= min_edge
    return new_edges, cost


def get_min_index(weights, current, visited):  # time - O(n)
    min_weight = float('inf')
    min_index = len(weights)
    for i, weight in enumerate(weights):  # time = O(n)
        if weight < min_weight and i != current and i not in visited:
            min_weight = weight
            min_index = i
    return min_index


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:  # time = O(n^3), space = O(n^2)
    solutions = []  # space = O(n^2) - holds up to n solutions each of length n
    best = float('inf')
    for i in range(len(edges)):  # time = O(n) - tries all possible starting positions
        visited = set()  # space = O(n)
        visited.add(i)
        current = i
        solution = [i]  # space = O(n)
        while len(visited) != len(edges):  # time = O(n)
            next_node = get_min_index(edges[current], current, visited)  # time = O(n)
            if next_node == len(edges):  # no neighbors
                break
            current = next_node
            visited.add(current)
            solution.append(current)
        time_out = timer.time_out()
        if time_out:
            return solutions
        else:
            score = score_tour(solution, edges)
            time = timer.time()
            if len(solution) == len(edges) and edges[current][i] != float('inf') and score < best:
                solutions.append(SolutionStats(solution, score, time, 0, 0, 0, 0, 0))
                best = score
    return solutions


def is_solution(current, i, last_node, edges):  # time/space = O(1)
    if len(current) + 1 != len(edges):
        return False
    elif edges[last_node][i] == float('inf'):
        return False
    else:
        return True
    
    
def dfs(best, timer, edges):
    solutions = []  # space = O(n^2) - up to n solutions each of size n
    stack = [[0]]  # up to n!
    while stack and not timer.time_out():
        current = stack.pop()
        last_node = current[-1]
        visited = set()
        for node in current:  # Time - up to O(n)
            visited.add(node)
        for i in range(1, len(edges)):  # Time - up to O(n)
            if i not in visited:
                if is_solution(current, i, last_node, edges):
                    solution = current.copy()  # space / time = O(n)
                    solution.append(i)
                    score = score_tour(solution, edges)
                    if score < best:
                        best = score
                        time = timer.time()
                        solutions.append(SolutionStats(solution, score, time, 0, 0, 0, 0, 0))
                else:
                    possible_path = current.copy()  # space / time = O(n)
                    possible_path.append(i)
                    stack.append(possible_path)
    return solutions


def b_and_b(best, timer, edges):
    solutions = []  # space = O(n^2) - up to n solutions each of size n
    for i in range(len(edges)):
        edges[i][i] = float('inf')
    reduced_matrix, cost = get_reduced_cost_matrix(edges)
    stack = [([0], cost, reduced_matrix)]  # up to n!
    while stack and not timer.time_out():
        current_path, current_cost, current_reduced_matrix = stack.pop()
        last_node = current_path[-1]
        visited = set()
        for node in current_path:  # Time - up to O(n)
            visited.add(node)
        for i in range(1, len(edges)):  # Time - up to O(n)
            if i not in visited:
                if is_solution(current_path, i, last_node, edges):
                    solution = current_path.copy()  # space / time = O(n)
                    solution.append(i)
                    score = score_tour(solution, edges)
                    if score < best:
                        best = score
                        time = timer.time()
                        solutions.append(SolutionStats(solution, score, time, 0, 0, 0, 0, 0))
                else:
                    possible_path = current_path.copy()  # space / time = O(n)
                    start = possible_path[-1]
                    possible_path.append(i)
                    end = possible_path[-1]
                    matrix, min_cost = block_rows_and_cols(current_reduced_matrix, start, end, current_path)
                    min_cost += (cost + edges[end][start])
                    if min_cost < best:
                        stack.append((possible_path, min_cost, matrix))
    return solutions


def backtracking(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    best = float('inf')
    return dfs(best, timer, edges)


def branch_and_bound(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    best = float('inf')
    solutions = greedy_tour(edges, timer)
    for solution in solutions:
        if solution.score < best:
            best = solution.score
    # print(f"best = {best}")
    solutions.extend(b_and_b(best, timer, edges))
    # print(f"solutions = {solutions}")
    return solutions


def branch_and_bound_smart(
    edges: list[list[float]], timer: Timer
) -> list[SolutionStats]:
    return []
