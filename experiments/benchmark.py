import os
import time
import statistics
import csv
import datetime
from puzzles.config import GOAL_STATE
from puzzles.puzzle import PuzzleState
from puzzles.heuristics import compute_h
from puzzles.helpers import generate_random_board
from puzzles.search import a_star_search


def run_single_experiment(start_board, heuristic_method):
    """
    Run A* on a specific board with the specified heuristic.
    """
    start_state = PuzzleState(start_board)
    start_state.h = compute_h(start_board, GOAL_STATE, heuristic_method)
    start_state.f = start_state.g + start_state.h

    start_time = time.time()
    solution_path, expanded_nodes = a_star_search(start_state, GOAL_STATE, heuristic_method)
    end_time = time.time()

    runtime = end_time - start_time
    moves = (len(solution_path) - 1) if solution_path else -1
    return moves, expanded_nodes, runtime


def print_summary(heuristic, results, n):
    """
    Print a clearly labeled statistical summary.
    """
    moves_mean = statistics.mean(results["moves"])
    moves_std = statistics.stdev(results["moves"]) if len(results["moves"]) > 1 else 0.0
    nodes_mean = statistics.mean(results["nodes"])
    nodes_std = statistics.stdev(results["nodes"]) if len(results["nodes"]) > 1 else 0.0
    time_mean = statistics.mean(results["times"])
    time_std = statistics.stdev(results["times"]) if len(results["times"]) > 1 else 0.0

    print(f"\n--- {heuristic.capitalize()} Heuristic Summary ({n} runs) ---")
    print(f"Mean number of solution moves:             {moves_mean:.2f}")
    print(f"Standard deviation of solution moves:      {moves_std:.2f}")
    print(f"Mean number of expanded nodes:             {nodes_mean:.2f}")
    print(f"Standard deviation of expanded nodes:      {nodes_std:.2f}")
    print(f"Mean runtime (seconds):                    {time_mean:.4f}")
    print(f"Standard deviation of runtime (seconds):   {time_std:.4f}")


def run_benchmark(n=100, save_csv=True, out_dir="results"):
    """
    Run benchmark with SAME boards for both heuristics.
    """
    os.makedirs(out_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    runs_path = os.path.join(out_dir, f"benchmark_runs_{timestamp}.csv")
    summary_path = os.path.join(out_dir, f"benchmark_summary_{timestamp}.csv")

    # Generate all boards ONCE
    boards = [generate_random_board() for _ in range(n)]

    results = {
        "hamming": {"moves": [], "nodes": [], "times": []},
        "manhattan": {"moves": [], "nodes": [], "times": []}
    }

    # Experimente immer ausführen, CSV optional speichern
    for heuristic in ["hamming", "manhattan"]:
        print(f"\n{'=' * 70}")
        print(f"Running {n} experiments with '{heuristic}' heuristic")
        print('=' * 70)

        # Öffne CSV-Datei nur, wenn speichern aktiviert ist
        csv_file = open(runs_path, "w", newline="") if save_csv else None
        writer = csv.writer(csv_file) if save_csv else None
        if save_csv:
            writer.writerow(["heuristic", "run", "moves", "nodes_expanded", "runtime_seconds"])

        for i, board in enumerate(boards):
            moves, nodes, runtime = run_single_experiment(board, heuristic)
            results[heuristic]["moves"].append(moves)
            results[heuristic]["nodes"].append(nodes)
            results[heuristic]["times"].append(runtime)

            if save_csv:
                writer.writerow([heuristic, i + 1, moves, nodes, f"{runtime:.6f}"])

            print(
                f"Run #{i + 1:3}: "
                f"moves={moves:2}, "
                f"nodes_expanded={nodes:4}, "
                f"runtime={runtime:.4f}s"
            )

        print_summary(heuristic, results[heuristic], n)

        if save_csv:
            csv_file.close()

    # Save summary
    if save_csv:
        with open(summary_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "heuristic", "total_runs",
                "moves_mean", "moves_std",
                "nodes_mean", "nodes_std",
                "time_mean_seconds", "time_std_seconds"
            ])

            for heuristic in ["hamming", "manhattan"]:
                mv, nd, tm = results[heuristic]["moves"], results[heuristic]["nodes"], results[heuristic]["times"]
                writer.writerow([
                    heuristic, len(mv),
                    f"{statistics.mean(mv):.4f}", f"{statistics.stdev(mv) if len(mv) > 1 else 0:.4f}",
                    f"{statistics.mean(nd):.4f}", f"{statistics.stdev(nd) if len(nd) > 1 else 0:.4f}",
                    f"{statistics.mean(tm):.6f}", f"{statistics.stdev(tm) if len(tm) > 1 else 0:.6f}"
                ])

        print(f"\n{'=' * 70}\n📁 FILES SAVED\n{'=' * 70}")
        print(f"✅ Detailed run results: {runs_path}")
        print(f"✅ Statistical summary:  {summary_path}\n{'=' * 70}")

    return results

if __name__ == "__main__":
    run_benchmark(n=100, save_csv=True)
