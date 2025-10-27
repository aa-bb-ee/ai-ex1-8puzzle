import os
import pytest
import experiments.benchmark as benchmark
from puzzles.helpers import generate_random_board, is_solvable


@pytest.mark.parametrize("heuristic", ["hamming", "manhattan"])
def test_run_single_experiment_returns_valid(heuristic):
    """run_single_experiment should return plausible types/ranges."""
    # Create a random, solvable board
    board = generate_random_board()
    moves, nodes, runtime = benchmark.run_single_experiment(board, heuristic)

    # Type checks
    assert isinstance(moves, int)
    assert isinstance(nodes, int)
    assert isinstance(runtime, float)

    # Basic sanity checks
    assert nodes >= 0
    assert runtime >= 0.0


def test_run_benchmark_collects_data(monkeypatch):
    """run_benchmark should fill expected structures for both heuristics."""

    # Replace run_single_experiment with a deterministic dummy
    def dummy_experiment(board, heuristic):
        return 5, 20, 0.01  # moves, nodes, runtime

    monkeypatch.setattr(benchmark, "run_single_experiment", dummy_experiment)

    # Run without writing CSVs
    results = benchmark.run_benchmark(n=5, save_csv=False)

    # Check structure and lengths
    for heuristic in ["hamming", "manhattan"]:
        assert set(results[heuristic].keys()) == {"moves", "nodes", "times"}
        assert len(results[heuristic]["moves"]) == 5
        assert len(results[heuristic]["nodes"]) == 5
        assert len(results[heuristic]["times"]) == 5

        # Values should match the dummy outputs
        assert all(m == 5 for m in results[heuristic]["moves"])
        assert all(n == 20 for n in results[heuristic]["nodes"])
        assert all(abs(t - 0.01) < 1e-6 for t in results[heuristic]["times"])


def test_csv_output(tmp_path):
    """A basic CSV write/read roundtrip should succeed."""
    csv_path = tmp_path / "test.csv"

    # Write a small CSV file
    import csv
    data = [
        ["heuristic", "run", "moves", "nodes_expanded", "runtime_seconds"],
        ["hamming", 1, 5, 20, 0.01],
        ["manhattan", 1, 6, 22, 0.02],
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    # Verify the file exists and has 3 lines (header + 2 rows)
    assert csv_path.exists()
    with open(csv_path) as f:
        lines = f.readlines()
    assert len(lines) == 3


def test_run_benchmark_creates_csv_files(monkeypatch, tmp_path):
    """With save_csv=True, run_benchmark should create two CSVs (runs + summary)."""
    def dummy_experiment(board, heuristic):
        return 3, 10, 0.001

    monkeypatch.setattr(benchmark, "run_single_experiment", dummy_experiment)

    out_dir = tmp_path / "results"
    results = benchmark.run_benchmark(n=2, save_csv=True, out_dir=out_dir)

    # Basic result presence check
    assert isinstance(results, dict)
    assert "hamming" in results and "manhattan" in results

    # Check that exactly one runs CSV and one summary CSV were created
    files = list(out_dir.iterdir())
    run_files = [f for f in files if "benchmark_runs_" in f.name]
    summary_files = [f for f in files if "benchmark_summary_" in f.name]

    assert len(run_files) == 1
    assert len(summary_files) == 1


def test_generate_random_board_produces_solvable():
    """generate_random_board should always produce a solvable board."""
    for _ in range(10):
        board = generate_random_board()
        assert is_solvable(board)
