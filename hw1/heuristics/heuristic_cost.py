def hn_uniform(board, goal, grid):
    """
    Uniform Cost Search, h(n) = 0
    """
    return 0


def hn_misplaced(board, goal, grid):
    """
    Misplaced Tiles Heuristic, h(n) = # of misplaced digit except 0

    Construct goal state board base on len(board)
    Automatically supports puzzles of arbitrary square sizes (3x3, 4x4, ...)
    """
    #goal = list(range(1, len(board))) + [0] # construct goal board
    hn = 0
    for i in range(len(board)):
        if board[i] == 0:
            continue
        if board[i] != goal[i]:
            hn += 1

    return hn


def hn_manhattan(board, goal, grid):
    """
    Manhattan Distance Heuristic, h(n) = sum of x/y coordinate distance

    Construct goal state board base on len(board)
    Automatically supports puzzles of arbitrary square sizes (3x3, 4x4, ...)
    """
    # grid = int(len(board) ** 0.5) # calculate the square size of puzzle
    # goal = list(range(1, len(board))) + [0] # construct goal board
    hn = 0
    for i in range(len(board)):
        if board[i] == 0:
            continue
        curr_num = board[i]
        # transform 1D array location to the coordinate of 2D
        curr_row, curr_col = i // grid, i % grid
        right_index = goal.index(curr_num)
        # transform 1D array location to the coordinate of 2D
        right_row, right_col = right_index // grid, right_index % grid
        hn += abs(right_row - curr_row) + abs(right_col - curr_col)

    return hn

