# Project Report - Branch and Bound

## Baseline

### Design Experience

* I met with Lily Nahoopii, and we mostly reviewed the basic algorithm for creating the reduced
cost matrix. I decided to just create a copy of the edges array to use as the reduced cost matrix 

### Theoretical Analysis - Reduced Cost Matrix

#### Time 

* **O(n^2)** - there are 2 things that happen in sequence that are both O(n^2) The first is copying
the edges matrix, and the second is doing the reductions to the rows and columns, each of which take O(n^2) time

```python
def get_reduced_cost_matrix(edges: list[list[float]]):  # overall space / time = O(n^2)
    cost = 0
    new_edges = edges.copy()  # time/space = O(n^2)

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
        for k in range(len(new_edges)):  # time = O(n)
            new_edges[k][i] -= min_edge
    return new_edges, cost
```

#### Space

* **O(n^2)** The data structure that takes up the most space is the copy of the edges matrix. This will take up n^2 space,
but it's modified in place, so it doesn't take up extra space.

```python
def get_reduced_cost_matrix(edges: list[list[float]]):  # overall space / time = O(n^2)
    cost = 0
    new_edges = edges.copy()  # time/space = O(n^2)

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
        for k in range(len(new_edges)):  # time = O(n)
            new_edges[k][i] -= min_edge
    return new_edges, cost
```

## Core

### Design Experience

* I talked with Lily Nahoopii, and we reviewed the algorithm for branch and bound. We discussed why it would be
faster than backtracking and the different rules for pruning. 

### Theoretical Analysis - Branch and Bound TSP

#### Time 

*Fill me in*

#### Space

*Fill me in*

### Empirical Data

| N   | time (ms) |
|-----|-----------|
| 5   |           |
| 10  |           |
| 15  |           |
| 20  |           |
| 30  |           |
| 50  |           |

### Comparison of Theoretical and Empirical Results

- Empirical order of growth: 
- Measured constant of proportionality: 

![img](img.png)

*Fill me in*

## Stretch 1 

### Design Experience

*Fill me in*

### Search Space Over Time

![Plot demonstrating search space explored over time]()

*Fill me in*

## Stretch 2

### Design Experience

*Fill me in*

### Selected PQ Key

*Fill me in*

### Branch and Bound versus Smart Branch and Bound

*Fill me in*

## Project Report 

* I met with Lily Nahoopii, and we discussed our implementations for baseline as well as our tests. We both had a very similar approach to 
the reduced cost matrix algorithm and the tests, testing input that did and didn't include infinity values. She added a check in the reduced
cost matrix algorithm for the min being 0, which I think makes it slightly faster as it doesn't have to loop through subtracting 0 from everything.

