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
    # Swap the blank (index 8) with tile 8 (index 7) -> one move away
    start = [1, 2, 3,
             4, 5, 6,
             7, 0, 8]
    assert hamming_distance(start, GOAL_STATE) == 1
    assert manhattan_distance(start, GOAL_STATE) == 1


def test_if_two_swaps_adjacent_to_blank_goal_state_has_two_costs():
    # Two tiles (5 and 6) are misplaced by one column each
    start = [1, 2, 3,
             4, 6, 5,
             7, 8, 0]
    # Hamming counts misplaced tiles (5 and 6) => 2
    assert hamming_distance(start, GOAL_STATE) == 2
    # Manhattan: 5 is one step from col 1 to col 2, 6 is one step back => 1 + 1 = 2
    assert manhattan_distance(start, GOAL_STATE) == 2


def test_tile_far_from_goal_corner_case():
    # Tile 1 is in bottom-right corner; goal wants it at index 1
    start = [0, 2, 3,
             4, 5, 6,
             7, 8, 1]
    # Hamming: only tile 1 is misplaced (blank ignored) => 1
    assert hamming_distance(start, GOAL_STATE) == 1
    # Manhattan for tile 1: from (2,2) to (0,0) => |2-0| + |2-0| = 4
    assert manhattan_distance(start, GOAL_STATE) == 4


def test_blank_is_ignored():
    # Only blank moved; all numbered tiles are correct
    start = [1, 0, 2,
             3, 4, 5,
             6, 7, 8]
    assert hamming_distance(start, GOAL_STATE) == 0
    assert manhattan_distance(start, GOAL_STATE) == 0



def test_compute_h_selector():
    start = [1, 2, 3,
             4, 0, 6,
             7, 5, 8]
    # Hamming: tiles 5 and 8 are misplaced => 2
    assert compute_h(start, GOAL_STATE, "hamming") == 2
    # Manhattan: 5 is 1 step down-right, 8 is 1 step right/up relative to blank location -> total 2
    assert compute_h(start, GOAL_STATE, "manhattan") == 2


def test_manhattan_dominates_hamming_on_various_states():
    """For random permutations (not necessarily all solvable), Manhattan >= Hamming."""
    for _ in range(100):
        state = list(range(9))
        random.shuffle(state)
        h_h = hamming_distance(state, GOAL_STATE)
        h_m = manhattan_distance(state, GOAL_STATE)
        assert h_m >= h_h


def test_multiple_misplacements_manhattan_adds_up():
    # Move 7 and 8 to the second row, blank to bottom-left
    start = [1, 2, 3,
             4, 7, 8,
             0, 5, 6]
    # Hamming: tiles 5,6,7,8 are misplaced => 4
    assert hamming_distance(start, GOAL_STATE) == 4
    # Manhattan distances:
    # 5: from (2,1) -> (1,1): 1
    # 6: from (2,2) -> (1,2): 1
    # 7: from (1,1) -> (2,0): |1-2| + |1-0| = 2
    # 8: from (1,2) -> (2,1): |1-2| + |2-1| = 2
    # total = 1 + 1 + 2 + 2 = 6
    assert manhattan_distance(start, GOAL_STATE) == 6
