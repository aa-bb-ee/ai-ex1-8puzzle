# tests/test_puzzle.py

import pytest
from puzzles.puzzle import format_board, PuzzleState


# ---------- Tests for format_board (Emoji) & __str__ ----------

class TestFormatBoardEmoji:
    def test_format_board_returns_correct_emojis(self):
        """format_board should map numbers→emoji and show 0 as ⚫."""
        board = [
            1, 2, 3,
            4, 0, 5,
            6, 7, 8
        ]
        s = format_board(board)
        expected = "\n".join([
            "1️⃣ 2️⃣ 3️⃣",
            "4️⃣ ⚫ 5️⃣",
            "6️⃣ 7️⃣ 8️⃣",
        ])
        assert s == expected

    def test_str_returns_same_as_format_board(self):
        """PuzzleState.__str__ should delegate to format_board(board)."""
        board = [
            1, 2, 3,
            4, 0, 5,
            6, 7, 8
        ]
        state = PuzzleState(board)
        assert str(state) == format_board(board)


# ---------- Tests for neighbors ----------

class TestNeighbors:
    def test_neighbors_center_has_4_moves(self):
        """If empty tile is in the middle → 4 possible neighbors."""
        state = PuzzleState([
            1, 2, 3,
            4, 0, 5,
            6, 7, 8
        ])
        neighbors = state.neighbors()
        assert len(neighbors) == 4

    def test_neighbors_corner_has_2_moves(self):
        """If empty tile is in the corner → 2 possible neighbors."""
        state = PuzzleState([
            0, 1, 2,
            3, 4, 5,
            6, 7, 8
        ])
        neighbors = state.neighbors()
        assert len(neighbors) == 2

    def test_neighbors_edge_has_3_moves(self):
        """If empty tile is in the upper center → 3 possible neighbors."""
        state = PuzzleState([
            1, 0, 2,
            3, 4, 5,
            6, 7, 8
        ])
        neighbors = state.neighbors()
        assert len(neighbors) == 3

    def test_each_neighbor_differs_by_one_swap(self):
        """Each neighbor muss differ after swapping the 0"""
        state = PuzzleState([
            1, 2, 3,
            4, 0, 5,
            6, 7, 8
        ])
        for n in state.neighbors():
            diffs = [i for i, (a, b) in enumerate(zip(state.board, n.board)) if a != b]
            # Only 2 separate positions (the swapped tiles)
            assert len(diffs) == 2
            assert 0 in [n.board[i] for i in diffs]

    def test_g_value_increases_by_one(self):
        """After generating a neighbor g has to increase by 1."""
        state = PuzzleState([
            1, 2, 3,
            4, 0, 5,
            6, 7, 8
        ], g=2)
        for n in state.neighbors():
            assert n.g == state.g + 1


# ---------- Tests for comparison & hash ----------

class TestEqualityAndOrdering:
    def test_equality_and_hash(self):
        """States with identical boards are equal and hash-identical."""
        a = PuzzleState([1, 2, 3, 4, 0, 5, 6, 7, 8])
        b = PuzzleState([1, 2, 3, 4, 0, 5, 6, 7, 8])
        c = PuzzleState([1, 2, 3, 4, 5, 0, 6, 7, 8])

        assert a == b
        assert hash(a) == hash(b)
        assert a != c
        assert hash(a) != hash(c)


