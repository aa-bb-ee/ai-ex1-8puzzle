import time
import statistics
import csv
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
    moves_std = statistics.stdev(results["moves"])
    nodes_mean = statistics.mean(results["nodes"])
    nodes_std = statistics.stdev(results["nodes"])
    time_mean = statistics.mean(results["times"])
    time_std = statistics.stdev(results["times"])
    print(f"\n--- {heuristic.capitalize()} Heuristic Summary ({n} runs) ---")
    print(f"Mean number of solution moves:             {moves_mean:.2f}")
    print(f"Standard deviation of solution moves:      {moves_std:.2f}")
    print(f"Mean number of expanded nodes:             {nodes_mean:.2f}")
    print(f"Standard deviation of expanded nodes:      {nodes_std:.2f}")
    print(f"Mean runtime (seconds):                    {time_mean:.4f}")
    print(f"Standard deviation of runtime (seconds):   {time_std:.4f}")

def run_benchmark(n=100, save_csv=False):
    """
    Run the benchmark experiment for both heuristics with detailed output.
    """
    results = {"hamming": {"moves": [], "nodes": [], "times": []},
               "manhattan": {"moves": [], "nodes": [], "times": []}}

    for heuristic in ["hamming", "manhattan"]:
        print(f"\n##### Running {n} experiments with '{heuristic}' heuristic #####")
        for i in range(n):
            moves, nodes, runtime = run_single_experiment(heuristic)
            results[heuristic]["moves"].append(moves)
            results[heuristic]["nodes"].append(nodes)
            results[heuristic]["times"].append(runtime)
            print(
                f"Run #{i+1:3}: "
                f"moves={moves}, "
                f"nodes_expanded={nodes}, "
                f"runtime_seconds={runtime:.4f}"
            )
        print_summary(heuristic, results[heuristic], n)

    if save_csv:
        with open("benchmark_results.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["heuristic", "run", "moves", "nodes_expanded", "runtime_seconds"])
            for heuristic in ["hamming", "manhattan"]:
                for i in range(n):
                    writer.writerow([heuristic, i+1,
                                     results[heuristic]["moves"][i],
                                     results[heuristic]["nodes"][i],
                                     results[heuristic]["times"][i]])
        print("\nAll detailed results saved to 'benchmark_results.csv'.")
    return results

if __name__ == "__main__":
    run_benchmark(n=100, save_csv=True)

