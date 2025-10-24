# tests/test_heuristics.py
import unittest

import random

from puzzles.heuristics import (
    hamming_distance,
    manhattan_distance,
    compute_h,
)

from puzzles.config import GOAL_STATE


def test_if_correct_order_goal_state_has_zero_cost_with_hamming_and_manhattan():
    start = GOAL_STATE[:]
    assert hamming_distance(start, GOAL_STATE) == 0
    assert manhattan_distance(start, GOAL_STATE) == 0
    assert compute_h(start, GOAL_STATE, "hamming") == 0
    assert compute_h(start, GOAL_STATE, "manhattan") == 0


def test_if_single_swap_adjacent_to_blank_goal_state_has_one_cost():
    # Swap the blank (0) with tile 1 -> one move away from goal
    start = [0, 1, 2,
             3, 5, 4,
             6, 7, 8]
    # Hamming counts both misplaced tiles
    assert hamming_distance(start, GOAL_STATE) == 2
    # Manhattan sums both distances (1 + 1)
    assert manhattan_distance(start, GOAL_STATE) == 2


def test_if_two_swaps_adjacent_to_blank_goal_state_has_two_costs():
    # Two tiles (4 and 5) are swapped — each one column away
    start = [0, 1, 2,
             3, 5, 4,
             6, 7, 8]
    # Hamming counts misplaced tiles (5 and 6) => 2
    assert hamming_distance(start, GOAL_STATE) == 2
    # Manhattan: 5 is one step from col 1 to col 2, 6 is one step back => 1 + 1 = 2
    assert manhattan_distance(start, GOAL_STATE) == 2


def test_tile_far_from_goal_corner_case():
    # Tile 1 is in the bottom-right corner instead of top-left (goal position)
    # Tile 8 is swapped with it
    start = [0, 8, 2,
             3, 4, 5,
             6, 7, 1]
    # Hamming: tiles 1 and 8 are misplaced
    assert hamming_distance(start, GOAL_STATE) == 2
    # Manhattan: 1 moves from (2,2) -> (0,1) = 3; 8 moves from (0,1) -> (2,2) = 3 → total = 6
    assert manhattan_distance(start, GOAL_STATE) == 6


def test_blank_is_ignored():
    # Only blank moved; the swapped numbered tile is counted, not the blank
    start = [1, 0, 2,
             3, 4, 5,
             6, 7, 8]
    # Tile 1 is misplaced, blank ignored
    assert hamming_distance(start, GOAL_STATE) == 1
    assert manhattan_distance(start, GOAL_STATE) == 1


def test_compute_h_selector():
    # Ensure compute_h correctly delegates to both heuristics
    start = [0, 1, 2,
             3, 5, 4,
             6, 7, 8]
    assert compute_h(start, GOAL_STATE, "hamming") == 2
    assert compute_h(start, GOAL_STATE, "manhattan") == 2


def test_manhattan_dominates_hamming_on_various_states():
    """For random permutations (not necessarily solvable), Manhattan ≥ Hamming."""
    for _ in range(100):
        state = list(range(9))
        random.shuffle(state)
        h_h = hamming_distance(state, GOAL_STATE)
        h_m = manhattan_distance(state, GOAL_STATE)
        assert h_m >= h_h


def test_multiple_misplacements_manhattan_adds_up():
    # Several tiles are misplaced; Manhattan should accumulate their distances
    start = [0, 1, 2,
             7, 8, 5,
             6, 4, 3]
    # Hamming: tiles 4, 5, 7, 8 are misplaced
    assert hamming_distance(start, GOAL_STATE) == 4
    # Manhattan: total distance = 8
    assert manhattan_distance(start, GOAL_STATE) == 8