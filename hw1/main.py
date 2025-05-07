import sys
from search import a_star, trace_print
from heuristics import hn_uniform, hn_manhattan, hn_misplaced


def solvable_checker(board, grid):
    """
    Check if the board is solvable based on inversion count and grid size

    For odd grid:
        - solvable, if the inversions is even, the puzzle is solvable.

    For even grid, count the row index of `0` from the bottom:
        - solvable, if `0` is on even row from bottom and inversion is odd
        - solvable, if `0` is on odd row from bottom and inversion is even
    """
    #grid = int(len(board) ** 0.5) # grid size

    inversion = 0
    for i in range(len(board)): # count the inversion num
        for j in range(i + 1, len(board)):
            if (board[i] != 0 and board[j] != 0 and board[i] > board[j]):
                inversion += 1

    if grid % 2 == 1: # odd grid
        return inversion % 2 == 0
    else: # even grid
        row_of_zero_bottom = grid - (board.index(0) // grid)
        if row_of_zero_bottom % 2 == 0:
            return inversion % 2 == 1
        else:
            return inversion % 2 == 0


def parser():
    """
    Parse the command line
    """
    heuristic_map = {
        "uniform": hn_uniform,
        "misplaced": hn_misplaced,
        "manhattan": hn_manhattan
    }

    # check the input num
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <start_board> <heuristic>")
        print("heuristic: uniform, misplaced, manhattan")
        print('Example: python3 main.py "6 5 1 3 2 8 7 4 0" manhattan')
        sys.exit(1)

    # check the input board is integer
    start_input = sys.argv[1].strip()
    heuristic_name = sys.argv[2].strip().lower()
    try:
        start_board = [int(n) for n in start_input.split()]
    except:
        print("[Error - board] ensure all inputs are integers.")
        sys.exit(1)

    # check the num range
    expected_set = set(range(len(start_board)))
    input_set = set(start_board)
    if input_set != expected_set:
        print(f"[Error - board] ensure input contain all values from 0 to {len(start_board)-1}.")
        sys.exit(1)

    # check the grid
    grid = int(len(start_board) ** 0.5)
    if grid * grid != len(start_board):
        print("[Error - board] the board must be square like 3*3.")
        sys.exit(1)

    # check the heuristic
    if heuristic_name not in heuristic_map:
        print("[Error - heuristic] choose from: uniform, misplaced, manhattan.")
        sys.exit(1)

    hn_func = heuristic_map[heuristic_name]
    goal = list(range(1, len(start_board))) + [0] # construct goal

    return start_board, goal, hn_func, grid


def main():
    start_board, goal, hn_func, grid = parser()

    # check solvable
    if not solvable_checker(start_board, grid):
        print("This puzzle is not solvable.")
        sys.exit(1)

    # execute A*
    steps, path = a_star(start_board, goal, hn_func, grid)

    # out put
    if steps == -1:
        print("No solution found.")
    else:
        print(f"Solved in {steps} steps.")
        trace_print(path, grid)


if __name__ == "__main__":
    main()

