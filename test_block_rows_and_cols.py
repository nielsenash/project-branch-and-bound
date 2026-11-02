from tsp_solve import block_rows_and_cols


def test_block_rows_and_cols():
    initial_edges = [[1, 2, 3], [6, 3, 3], [4, 4, 8]]
    print(block_rows_and_cols(initial_edges, 0, 1, [0]))