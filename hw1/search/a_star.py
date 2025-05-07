from heapq import heappop, heappush


def neighbor_create(board, grid):
    """
    Create new board in 4 direction
    """
    neighbors = []
    zero_loc = board.index(0)
    # transform 1D location into 2D coordinate
    zero_row, zero_col = zero_loc // grid, zero_loc % grid

    direction = [(1,0), (-1,0), (0,1), (0,-1)] # up down right left
    for d_row, d_col in direction:
        new_row, new_col = zero_row + d_row, zero_col + d_col
        if 0 <= new_row < grid and 0 <= new_col < grid:
            # transform 2D coordinate into 1D location
            new_zero_loc = new_row * grid + new_col
            new_board = board.copy()
            # swap
            new_board[zero_loc], new_board[new_zero_loc] \
                            = new_board[new_zero_loc], new_board[zero_loc]
            neighbors.append(new_board)

    return neighbors


def a_star(start_board, goal, hn_func, grid):
    """
    A* search

    Parameters:
        - start_board: initial board (list)
        - goal: goal board (list)
        - hn_func: 1)hn_uniform, 2)hn_manhattan, 3)hn_misplaced
        - grid: grid size
    """
    visited = set()
    ancestors = {} # for reconstruct path usage
    ancestors[tuple(start_board)] = None
    fn_heap = []
    start_fn = hn_func(start_board, goal, grid) + 0
    heappush(fn_heap, (start_fn, 0, start_board)) # (fn, gn, board)

    while fn_heap:
        fn, gn, board = heappop(fn_heap)
        board_tuple = tuple(board)

        if board_tuple in visited: # if visited, pass
            continue
        if board == goal: # if reach the goal, return steps and path
            return gn, reconstruct_path(ancestors, board_tuple)
        visited.add(board_tuple)

        for neigh in neighbor_create(board, grid):
            neigh_tuple = tuple(neigh)
            if neigh_tuple in visited: # if neighbor is visited, pass
                continue
            ancestors[neigh_tuple] = board_tuple # record the new board's ancestor
            new_gn = gn + 1
            fn = new_gn + hn_func(neigh, goal, grid)
            heappush(fn_heap, (fn, new_gn, neigh)) # add into heap

    return -1, [] # error


def reconstruct_path(ancestors, curr_board):
    """
    Reconstruct path from start to current board using ancestors dict
    """
    path = [curr_board]
    while curr_board in ancestors:
        curr_board = ancestors[curr_board] # find the parent node
        path.append(curr_board)

    path.reverse()
    return path


def trace_print(path, grid):
    """
    Formated print the intermidiate state of board
    """
    for i, board in enumerate(path):
        print(f"In operation {i}, we have the board like below:")
        for row in range(grid):
            line = board[row * grid : (row + 1) * grid]
            formatted = " ".join("_" if n == 0 else str(n) for n in line)
            print(formatted)

