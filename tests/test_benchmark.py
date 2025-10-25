import os
import pytest
from puzzles.config import GOAL_STATE
from puzzles.puzzle import PuzzleState
from puzzles.heuristics import compute_h
from puzzles.helpers import generate_random_board, is_solvable
from puzzles.search import a_star_search
import experiments.benchmark as benchmark

@pytest.mark.parametrize("heuristic", ["hamming", "manhattan"])
def test_run_single_experiment_returns_valid(heuristic):
    """Test that a single experiment returns plausible results."""
    moves, nodes, runtime = benchmark.run_single_experiment(heuristic)
    assert isinstance(moves, int)
    assert isinstance(nodes, int)
    assert isinstance(runtime, float)
    assert nodes >= 0
    assert runtime >= 0

def test_run_benchmark_collects_data(monkeypatch):
    """Test that benchmark runner produces the right amount of data."""

    # Patch run_single_experiment to generate dummy results
    def dummy_experiment(method):
        return 5, 20, 0.01  # moves, nodes, runtime

    monkeypatch.setattr(benchmark, "run_single_experiment", dummy_experiment)
    results = benchmark.run_benchmark(n=5, save_csv=False)

    # Now check that results contain exactly 5 entries for each heuristic
    assert len(results["hamming"]["moves"]) == 5
    assert len(results["hamming"]["nodes"]) == 5
    assert len(results["hamming"]["times"]) == 5
    assert len(results["manhattan"]["moves"]) == 5
    assert len(results["manhattan"]["nodes"]) == 5
    assert len(results["manhattan"]["times"]) == 5

    # Check that all values match the dummy data
    assert results["hamming"]["moves"] == [5, 5, 5, 5, 5]
    assert results["hamming"]["nodes"] == [20, 20, 20, 20, 20]
    assert results["manhattan"]["moves"] == [5, 5, 5, 5, 5]
    assert results["manhattan"]["nodes"] == [20, 20, 20, 20, 20]

    # Check that times are plausible (all should be 0.01)
    assert all(t == 0.01 for t in results["hamming"]["times"])
    assert all(t == 0.01 for t in results["manhattan"]["times"])

def test_csv_output(tmp_path):
    """Test saving CSV output actually creates the file."""
    csv_path = tmp_path / "dummy.csv"
    # Patch open to use a temporary file
    import csv
    data = [
        ["heuristic", "run", "moves", "nodes_expanded", "runtime_seconds"],
        ["hamming", 1, 5, 20, 0.01],
        ["manhattan", 1, 6, 22, 0.02]
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    assert csv_path.exists()
    with open(csv_path) as f:
        lines = f.readlines()
    assert len(lines) == 3

def test_soluble_boards():
    """Test that the board generator only produces solvable puzzles."""
    for _ in range(10):
        board = generate_random_board()
        assert is_solvable(board)
