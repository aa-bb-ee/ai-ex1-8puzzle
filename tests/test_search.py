# tests/test_search.py

import pytest

from puzzles.config import GOAL_STATE as GOAL
from puzzles.puzzle import PuzzleState
from puzzles.heuristics import compute_h, manhattan_distance
from puzzles.search import a_star_search, reconstruct_path


# ------------------------------
# Helpers
# ------------------------------

def make_state(board, heuristic: str) -> PuzzleState:
    """
    Initialises a puzzleState incl. h and f for running a_star_search.
    """
    s = PuzzleState(board, g=0, h=0)
    s.h = compute_h(board, GOAL, heuristic)
    s.f = s.g + s.h
    return s


def neighbors_of_goal():
    """
    Generate all boards that are one legal move away from the GOAL.
    (Swaps the blank tile with each valid neighbor.)
    """
    bi = GOAL.index(0)
    r, c = divmod(bi, 3)
    result = []
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            ni = nr * 3 + nc
            b = GOAL[:]
            b[bi], b[ni] = b[ni], b[bi]
            result.append(b)
    return result


def apply_move(board, dr, dc):
    """
    Apply a single blank move (dr, dc) to a board.
    Returns a new board or None if the move is invalid.
    """
    bi = board.index(0)
    r, c = divmod(bi, 3)
    nr, nc = r + dr, c + dc
    if not (0 <= nr < 3 and 0 <= nc < 3):
        return None
    ni = nr * 3 + nc
    b = board[:]
    b[bi], b[ni] = b[ni], b[bi]
    return b


def apply_moves_from_goal(moves):
    """
    Generate a board by applying a sequence of blank moves starting from GOAL.
    Example: moves = [(0,1),(1,0)] → move blank right, then down.
    Returns None if any move is invalid.
    """
    b = GOAL[:]
    for dr, dc in moves:
        b = apply_move(b, dr, dc)
        if b is None:
            return None
    return b


# ------------------------------
# Test cases
# ------------------------------

@pytest.mark.parametrize("heuristic", ["hamming", "manhattan"])
def test_already_solved_returns_length_1_and_zero_expanded(heuristic):
    """If start == goal, the solution path should have length 1 and expand 0 nodes."""
    start = make_state(GOAL[:], heuristic)
    path, expanded = a_star_search(start, GOAL, heuristic)
    assert path is not None
    assert len(path) == 1
    assert path[0].board == GOAL
    assert expanded == 0


@pytest.mark.parametrize("heuristic", ["hamming", "manhattan"])
def test_one_move_away_solution(heuristic):
    """If the start is one move away from the goal, A* should solve it in 1 move."""
    nb = neighbors_of_goal()
    assert len(nb) >= 2  # For blank in top-left, there are 2 possible neighbors (Right, Down)
    start_board = nb[0]

    start = make_state(start_board, heuristic)
    path, expanded = a_star_search(start, GOAL, heuristic)

    assert path is not None
    assert path[0].board == start_board
    assert path[-1].board == GOAL

    assert len(path) - 1 == 1   # exactly one move
    assert expanded >= 0


@pytest.mark.parametrize("heuristic", ["hamming", "manhattan"])
def test_two_moves_away_solution_exact(heuristic):
    """
    Create a state two moves away from the goal (Right, Down).
    The optimal solution should require exactly 2 moves.
    """
    start_board = apply_moves_from_goal([(0, 1), (1, 0)])
    assert start_board is not None

    start = make_state(start_board, heuristic)
    path, expanded = a_star_search(start, GOAL, heuristic)

    assert path is not None
    assert path[0].board == start_board
    assert path[-1].board == GOAL
    assert len(path) - 1 == 2
    assert expanded >= 0
    # Manhattan distance is a lower bound for the true cost
    assert manhattan_distance(start_board, GOAL) <= 2


@pytest.mark.parametrize("heuristic", ["hamming", "manhattan"])
def test_path_is_sequence_of_single_blank_swaps(heuristic):
    """
    Each consecutive state in the path must differ by exactly one valid blank move.
    """
    start_board = apply_moves_from_goal([(0, 1), (1, 0), (0, 1)])
    assert start_board is not None

    start = make_state(start_board, heuristic)
    path, _ = a_star_search(start, GOAL, heuristic)
    assert path is not None

    for prev, nxt in zip(path, path[1:]):
        diffs = [i for i, (a, b) in enumerate(zip(prev.board, nxt.board)) if a != b]
        assert len(diffs) == 2      # two swapped tiles
        # Blank (0) must be one of the swapped tiles
        assert 0 in (prev.board[diffs[0]], prev.board[diffs[1]])
        assert 0 in (nxt.board[diffs[0]], nxt.board[diffs[1]])


@pytest.mark.parametrize("heuristic", ["hamming", "manhattan"])
def test_reconstruct_path_matches_search_output(heuristic):
    """Reconstructed path from the goal state should match the path returned by A*."""
    nb = neighbors_of_goal()
    start_board = nb[-1]

    start = make_state(start_board, heuristic)
    path, _ = a_star_search(start, GOAL, heuristic)
    assert path is not None

    # Reconstruct from end state and compare sequences
    end_state = path[-1]
    reconstructed = reconstruct_path(end_state)

    assert [s.board for s in reconstructed] == [s.board for s in path]


@pytest.mark.parametrize("heuristic", ["hamming", "manhattan"])
def test_solution_cost_is_bounded_by_applied_moves(heuristic):
    """
    If we generate a start state by applying K valid moves from the goal,
    then A* must find a solution with cost ≤ K (because the reverse path exists).
    """
    moves = [(0, 1), (1, 0), (1, 0), (0, 1)]  # Right, Down, Down, Right (all valid from upper left corner)
    start_board = apply_moves_from_goal(moves)
    assert start_board is not None

    start = make_state(start_board, heuristic)
    path, expanded = a_star_search(start, GOAL, heuristic)
    assert path is not None

    k = len(moves)
    assert (len(path) - 1) <= k
    assert expanded >= 0
