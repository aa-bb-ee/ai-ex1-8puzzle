import os
import pytest
import experiments.benchmark as benchmark
from puzzles.helpers import generate_random_board, is_solvable


@pytest.mark.parametrize("heuristic", ["hamming", "manhattan"])
def test_run_single_experiment_returns_valid(heuristic):
    """Test, dass run_single_experiment plausible Rückgabewerte liefert."""
    # Ein zufälliges, gültiges Board erzeugen
    board = generate_random_board()
    moves, nodes, runtime = benchmark.run_single_experiment(board, heuristic)

    # Typprüfungen
    assert isinstance(moves, int)
    assert isinstance(nodes, int)
    assert isinstance(runtime, float)

    # Werte sollten plausibel sein
    assert nodes >= 0
    assert runtime >= 0.0


def test_run_benchmark_collects_data(monkeypatch):
    """Test, dass run_benchmark die richtigen Datenstrukturen füllt."""

    # Dummy-Funktion ersetzt run_single_experiment
    def dummy_experiment(board, heuristic):
        return 5, 20, 0.01  # moves, nodes, runtime

    monkeypatch.setattr(benchmark, "run_single_experiment", dummy_experiment)

    # Benchmark ohne Dateiausgabe laufen lassen
    results = benchmark.run_benchmark(n=5, save_csv=False)

    # Struktur prüfen
    for heuristic in ["hamming", "manhattan"]:
        assert set(results[heuristic].keys()) == {"moves", "nodes", "times"}
        assert len(results[heuristic]["moves"]) == 5
        assert len(results[heuristic]["nodes"]) == 5
        assert len(results[heuristic]["times"]) == 5

        # Alle Werte müssen den Dummy-Ergebnissen entsprechen
        assert all(m == 5 for m in results[heuristic]["moves"])
        assert all(n == 20 for n in results[heuristic]["nodes"])
        assert all(abs(t - 0.01) < 1e-6 for t in results[heuristic]["times"])


def test_csv_output(tmp_path):
    """Test, dass CSV-Dateien korrekt erstellt werden."""
    csv_path = tmp_path / "test.csv"

    # CSV-Daten schreiben
    import csv
    data = [
        ["heuristic", "run", "moves", "nodes_expanded", "runtime_seconds"],
        ["hamming", 1, 5, 20, 0.01],
        ["manhattan", 1, 6, 22, 0.02],
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    # Datei prüfen
    assert csv_path.exists()
    with open(csv_path) as f:
        lines = f.readlines()
    assert len(lines) == 3


def test_run_benchmark_creates_csv_files(monkeypatch, tmp_path):
    """Test, dass run_benchmark bei save_csv=True zwei Dateien erstellt."""
    def dummy_experiment(board, heuristic):
        return 3, 10, 0.001

    monkeypatch.setattr(benchmark, "run_single_experiment", dummy_experiment)

    out_dir = tmp_path / "results"
    results = benchmark.run_benchmark(n=2, save_csv=True, out_dir=out_dir)

    # Ergebnisse prüfen
    assert isinstance(results, dict)
    assert "hamming" in results and "manhattan" in results

    # Dateien prüfen
    files = list(out_dir.iterdir())
    run_files = [f for f in files if "benchmark_runs_" in f.name]
    summary_files = [f for f in files if "benchmark_summary_" in f.name]

    assert len(run_files) == 1
    assert len(summary_files) == 1


def test_generate_random_board_produces_solvable():
    """Test, dass generierte Boards lösbar sind."""
    for _ in range(10):
        board = generate_random_board()
        assert is_solvable(board)
