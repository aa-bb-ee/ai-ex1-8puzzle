import random

def is_solvable(board):
    """Check if the given 8-puzzle board configuration is solvable."""
    # Remove the empty tile (represented by 0) since it doesn’t count for inversions
    arr = [x for x in board if x != 0]

    # Count inversions: how many pairs (i, j) exist where i < j but arr[i] > arr[j]
    inversions = sum(
        1 for i in range(len(arr)) for j in range(i + 1, len(arr)) if arr[i] > arr[j]
    )

    # For a 3x3 board, the puzzle is solvable if the inversion count is even
    return inversions % 2 == 0


def generate_random_board():
    """Generate a random, solvable 8-puzzle board configuration."""
    # Start with a list representing tiles 0–8 (0 is the empty space)
    board = list(range(9))

    # Randomly shuffle until the board is solvable
    random.shuffle(board)
    while not is_solvable(board):
        random.shuffle(board)

    # Return the solvable configuration
    return board
