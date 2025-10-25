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


def run_single_experiment(heuristic_method):
    """
    Run a single A* search with the specified heuristic.
    Returns number of moves, number of nodes expanded, and runtime in seconds.
    """
    start_board = generate_random_board()
    start_state = PuzzleState(start_board)
    start_state.h = compute_h(start_board, GOAL_STATE, heuristic_method)
    start_state.f = start_state.g + start_state.h

    start_time = time.time()
    solution_path, expanded_nodes = a_star_search(start_state, GOAL_STATE, heuristic_method)
    end_time = time.time()

    runtime = end_time - start_time
    moves = (len(solution_path) - 1) if solution_path else -1  # -1 indicates unsolved
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
    Run the benchmark experiment for both heuristics with detailed output.
    Saves two CSV files with timestamp:
    - benchmark_runs_TIMESTAMP.csv: all individual runs
    - benchmark_summary_TIMESTAMP.csv: statistical summary
    """
    # Create output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)

    # Generate timestamp for unique filenames
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    runs_filename = f"benchmark_runs_{timestamp}.csv"
    summary_filename = f"benchmark_summary_{timestamp}.csv"
    runs_path = os.path.join(out_dir, runs_filename)
    summary_path = os.path.join(out_dir, summary_filename)

    results = {
        "hamming": {"moves": [], "nodes": [], "times": []},
        "manhattan": {"moves": [], "nodes": [], "times": []}
    }

    # Run experiments and save detailed results
    if save_csv:
        with open(runs_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["heuristic", "run", "moves", "nodes_expanded", "runtime_seconds"])

            for heuristic in ["hamming", "manhattan"]:
                print(f"\n{'=' * 70}")
                print(f"Running {n} experiments with '{heuristic}' heuristic")
                print('=' * 70)

                for i in range(n):
                    moves, nodes, runtime = run_single_experiment(heuristic)
                    results[heuristic]["moves"].append(moves)
                    results[heuristic]["nodes"].append(nodes)
                    results[heuristic]["times"].append(runtime)

                    # Write to CSV immediately (streaming)
                    writer.writerow([heuristic, i + 1, moves, nodes, f"{runtime:.6f}"])

                    # Print progress
                    print(
                        f"Run #{i + 1:3}: "
                        f"moves={moves:2}, "
                        f"nodes_expanded={nodes:4}, "
                        f"runtime={runtime:.4f}s"
                    )

                # Print summary after each heuristic
                print_summary(heuristic, results[heuristic], n)
    else:
        # Run without saving CSV
        for heuristic in ["hamming", "manhattan"]:
            print(f"\n{'=' * 70}")
            print(f"Running {n} experiments with '{heuristic}' heuristic")
            print('=' * 70)

            for i in range(n):
                moves, nodes, runtime = run_single_experiment(heuristic)
                results[heuristic]["moves"].append(moves)
                results[heuristic]["nodes"].append(nodes)
                results[heuristic]["times"].append(runtime)

                print(
                    f"Run #{i + 1:3}: "
                    f"moves={moves:2}, "
                    f"nodes_expanded={nodes:4}, "
                    f"runtime={runtime:.4f}s"
                )

            print_summary(heuristic, results[heuristic], n)

    # Save summary statistics
    if save_csv:
        with open(summary_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "heuristic",
                "total_runs",
                "moves_mean", "moves_std",
                "nodes_mean", "nodes_std",
                "time_mean_seconds", "time_std_seconds"
            ])

            for heuristic in ["hamming", "manhattan"]:
                mv = results[heuristic]["moves"]
                nd = results[heuristic]["nodes"]
                tm = results[heuristic]["times"]

                moves_std = statistics.stdev(mv) if len(mv) > 1 else 0.0
                nodes_std = statistics.stdev(nd) if len(nd) > 1 else 0.0
                time_std = statistics.stdev(tm) if len(tm) > 1 else 0.0

                writer.writerow([
                    heuristic,
                    len(mv),
                    f"{statistics.mean(mv):.4f}", f"{moves_std:.4f}",
                    f"{statistics.mean(nd):.4f}", f"{nodes_std:.4f}",
                    f"{statistics.mean(tm):.6f}", f"{time_std:.6f}"
                ])

        print("\n" + "=" * 70)
        print("📁 FILES SAVED")
        print("=" * 70)
        print(f"✅ Detailed run results: {runs_path}")
        print(f"✅ Statistical summary:  {summary_path}")
        print("=" * 70)

    return results


if __name__ == "__main__":
    run_benchmark(n=100, save_csv=True)
