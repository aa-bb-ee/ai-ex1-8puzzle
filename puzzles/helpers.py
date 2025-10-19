import random

def is_solvable(board):
    """Check solvability using inversion count."""
    arr = [x for x in board if x != 0]
    inversions = sum(
        1 for i in range(len(arr)) for j in range(i+1, len(arr)) if arr[i] > arr[j]
    )
    return inversions % 2 == 0

def generate_random_board():
    """Generate a random solvable board."""
    board = list(range(9))
    random.shuffle(board)
    while not is_solvable(board):
        random.shuffle(board)
    return board
