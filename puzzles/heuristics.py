# puzzles/heuristics.py

def hamming_distance(board, goal):
    """
    Compute the Hamming distance between the current board and the goal.
    This heuristic counts the number of tiles that are not in their goal position,
    excluding the blank tile (represented by 0).

    Parameters:
    board (list): Current puzzle state as a list of 9 integers.
    goal (list): Goal puzzle state as a list of 9 integers.

    Returns:
    int: Number of misplaced tiles.
    """
    return sum(1 for i in range(9) if board[i] != 0 and board[i] != goal[i])


def manhattan_distance(board, goal):
    """
    Compute the Manhattan distance between the current board and the goal.
    This heuristic sums the vertical and horizontal distances each tile is away
    from its goal position, excluding the blank tile (0).

    Parameters:
    board (list): Current puzzle state as a list of 9 integers.
    goal (list): Goal puzzle state as a list of 9 integers.

    Returns:
    int: Total Manhattan distance.
    """
    distance = 0
    for i, tile in enumerate(board):
        if tile != 0:  # skip the blank
            goal_index = goal.index(tile)
            x1, y1 = divmod(i, 3)   # current row/col
            x2, y2 = divmod(goal_index, 3)  # goal row/col
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def compute_h(board, goal, method):
    """
    Select and compute the heuristic value for a given board state.

    Parameters:
    board (list): Current puzzle state as a list of 9 integers.
    goal (list): Goal puzzle state as a list of 9 integers.
    method (str): Heuristic method to use ("hamming" or "manhattan").

    Returns:
    int: Heuristic value based on the selected method.

    Raises:
    ValueError: If an unsupported method is passed.
    """
    if method == "hamming":
        return hamming_distance(board, goal)
    elif method == "manhattan":
        return manhattan_distance(board, goal)
    else:
        raise ValueError(f"Unsupported heuristic method: {method}")



