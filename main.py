import os
import time
import statistics
from puzzles.config import GOAL_STATE
from puzzles.helpers import generate_random_board
from puzzles.heuristics import compute_h
from puzzles.puzzle import PuzzleState
from puzzles.search import a_star_search


# ---------------------------------------------------------
# Run a single A* search experiment on a given puzzle board
# ---------------------------------------------------------
def run_single_experiment(start_board, heuristic_method):
    start_state = PuzzleState(start_board)
    start_state.h = compute_h(start_board, GOAL_STATE, heuristic_method)
    start_state.f = start_state.g + start_state.h

    start_time = time.time()
    solution_path, expanded_nodes = a_star_search(start_state, GOAL_STATE, heuristic_method)
    end_time = time.time()

    runtime = end_time - start_time
    moves = (len(solution_path) - 1) if solution_path else -1
    return moves, expanded_nodes, runtime, solution_path


# ---------------------------------------------------------
# Print mean and standard deviation of benchmark results
# ---------------------------------------------------------
def print_summary(heuristic, results, n):
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


# ---------------------------------------------------------
# Option 1: Solve a single random puzzle using both heuristics
# ---------------------------------------------------------
def option_1_solve_puzzle():
    print("\n🧩 Generating random solvable puzzle...")
    board = generate_random_board()
    start_state = PuzzleState(board)

    print("\nStart state:")
    print(start_state)

    print("\n🔎 Solving with both heuristics...")

    results = {}

    # Run both Manhattan and Hamming heuristics on the same puzzle
    for heuristic in ["manhattan", "hamming"]:
        moves, nodes, runtime, solution_path = run_single_experiment(board, heuristic)
        results[heuristic] = {"moves": moves, "nodes": nodes, "runtime": runtime, "path": solution_path}
        print(f"\n✅ {heuristic.capitalize()} heuristic solved: {moves} moves, {nodes} nodes expanded, {runtime:.4f}s")

    # Display comparison table
    print("\n📊 Comparison Table:")
    print(f"{'Heuristic':<10} {'Moves':<6} {'Nodes':<6} {'Runtime (s)':<10}")
    for heuristic in ["manhattan", "hamming"]:
        r = results[heuristic]
        print(f"{heuristic:<10} {r['moves']:<6} {r['nodes']:<6} {r['runtime']:<10.4f}")

    # Optionally show full solution paths
    show_path = input("\nShow solution paths? (y/n): ").strip().lower()
    if show_path == "y":
        for heuristic in ["manhattan", "hamming"]:
            print(f"\nSolution path for {heuristic}:")
            for step, state in enumerate(results[heuristic]["path"]):
                print(f"\nStep {step}:")
                print(state)


# ---------------------------------------------------------
# Option 2: Run benchmark over multiple random puzzles
# ---------------------------------------------------------
def option_2_benchmark(n_runs=100):
    print(f"\n🏁 Running benchmark with {n_runs} puzzles...")
    results = {"manhattan": {"moves": [], "nodes": [], "times": []},
               "hamming": {"moves": [], "nodes": [], "times": []}}

    # Generate all random boards once for fair comparison
    boards = [generate_random_board() for _ in range(n_runs)]

    # Run each heuristic on all generated boards
    for heuristic in ["manhattan", "hamming"]:
        for i, board in enumerate(boards, start=1):
            moves, nodes, runtime, _ = run_single_experiment(board, heuristic)
            results[heuristic]["moves"].append(moves)
            results[heuristic]["nodes"].append(nodes)
            results[heuristic]["times"].append(runtime)
            print(f"[{heuristic}] Run #{i}: moves={moves}, nodes={nodes}, time={runtime:.4f}s")

    # Display benchmark statistics table
    print("\n📊 Benchmark Comparison Table:")
    header = f"{'Heuristic':<10} | {'Mean Moves':<10} | {'Std Moves':<9} | {'Mean Nodes':<10} | {'Std Nodes':<9} | {'Mean Runtime (s)':<15} | {'Std Runtime (s)':<15}"
    print(header)
    print("-" * len(header))

    for heuristic in ["manhattan", "hamming"]:
        r = results[heuristic]
        moves_mean = statistics.mean(r["moves"])
        moves_std = statistics.stdev(r["moves"]) if len(r["moves"]) > 1 else 0.0
        nodes_mean = statistics.mean(r["nodes"])
        nodes_std = statistics.stdev(r["nodes"]) if len(r["nodes"]) > 1 else 0.0
        time_mean = statistics.mean(r["times"])
        time_std = statistics.stdev(r["times"]) if len(r["times"]) > 1 else 0.0

        print(f"{heuristic:<10} | {moves_mean:<10.2f} | {moves_std:<9.2f} | "
              f"{nodes_mean:<10.2f} | {nodes_std:<9.2f} | {time_mean:<15.4f} | {time_std:<15.4f}")


# ---------------------------------------------------------
# Option 3: Visualize and explain A* tie-breaking mechanism
# ---------------------------------------------------------
def option_3_tiebreak_demo():
    """Demonstrate tie-breaks in A* with visualization and user interaction."""
    import heapq, itertools

    # Helper: display board as emoji string for compact visualization
    def board_to_line_emoji(board):
        num_to_emoji = {
            0: '⚫', 1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣',
            5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣'
        }
        return ''.join(num_to_emoji[x] for x in board)

    print("\n🧩 Generating random puzzle for tie-break demonstration using Hamming heuristic...")
    board = generate_random_board()
    start_state = PuzzleState(board)
    start_state.h = compute_h(board, GOAL_STATE, "hamming")
    start_state.f = start_state.g + start_state.h

    print("\nStart state:")
    print(start_state)
    print("\n🔎 Solving while monitoring tie-breaks...")

    # Priority queue (min-heap) with tie-breaker counter
    frontier = []
    counter = itertools.count()
    heapq.heappush(frontier, (start_state.f, start_state.h, next(counter), start_state))
    explored = set()

    # A* main loop (with detailed tie-break visualization)
    while frontier:
        # Detect ties (nodes with same f-value)
        f_top = frontier[0][0]
        tie_nodes = [(f, h, c, n) for f, h, c, n in frontier if f == f_top]

        if len(tie_nodes) > 1:
            print("\n⚠️ Tie-break detected among the following nodes:")
            for f, h, c, node in tie_nodes:
                print(f"{board_to_line_emoji(node.board)} [f={f}, h={h}, count={c}]")

            # Select node by smallest h, then FIFO (earliest count)
            selected = min(tie_nodes, key=lambda x: (x[1], x[2]))
            print(f"\n➡ Selected node: {board_to_line_emoji(selected[3].board)} [f={selected[0]}, h={selected[1]}, count={selected[2]}]")
            print("Reason: smallest h, then earliest inserted (FIFO)")

            # Ask user whether to continue or stop demonstration
            cont = input("\nShow next tie-breaks? (y/n): ").strip().lower()
            if cont != "y":
                print("Aborting tie-break demonstration.")
                break

        # Expand next node
        _, _, _, current = heapq.heappop(frontier)

        # If goal reached → reconstruct full path
        if current.board == GOAL_STATE:
            path = []
            while current:
                path.append(current)
                current = getattr(current, "parent", None)
            path.reverse()
            print(f"\n✅ Puzzle solved in {len(path)-1} moves!")
            print("Solution path:")
            for step, state in enumerate(path):
                print(f"\nStep {step}: {state}")
            break

        # Expand neighbors and push to heap
        explored.add(current)
        for neighbor in current.neighbors():
            if neighbor in explored:
                continue
            neighbor.h = compute_h(neighbor.board, GOAL_STATE, "hamming")
            neighbor.g = current.g + 1
            neighbor.f = neighbor.g + neighbor.h
            neighbor.parent = current
            heapq.heappush(frontier, (neighbor.f, neighbor.h, next(counter), neighbor))


# ---------------------------------------------------------
# Interactive main menu for user interaction
# ---------------------------------------------------------
def main_menu():
    while True:
        print("\n" + "=" * 55)
        print("🎯  A* 8-Puzzle Interactive Menu")
        print("=" * 55)
        print("1️⃣  Solve a random puzzle using both heuristics")
        print("2️⃣  Run benchmark comparison")
        print("3️⃣  Demonstrate A* tie-breaking")
        print("0️⃣  Exit program")
        print("=" * 55)

        choice = input("⌨️  Enter your choice (0–3): ").strip()

        # Handle user menu choices
        if choice == "1":
            option_1_solve_puzzle()
        elif choice == "2":
            n = input("📊  Number of benchmark runs (default 100): ").strip()
            n_runs = int(n) if n.isdigit() else 100
            option_2_benchmark(n_runs)
        elif choice == "3":
            option_3_tiebreak_demo()
        elif choice == "0":
            print("\nExiting program. Goodbye!\n")
            break
        else:
            print("\n⚠️  Invalid choice! Please enter a number between 0 and 3.")


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    main_menu()
