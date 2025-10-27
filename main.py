import os
import time
from puzzles.config import GOAL_STATE
from puzzles.helpers import generate_random_board
from puzzles.heuristics import compute_h
from puzzles.puzzle import PuzzleState
from puzzles.search import a_star_search

def main():
    """Run a single A* solve on a random solvable 8-puzzle board and print results."""

    # Generate a random solvable board
    start_board = generate_random_board()
    start_state = PuzzleState(start_board)
    print("\n🧩 Start State:")
    print(start_state)

    # Choose the heuristic method here: "hamming" or "manhattan"
    heuristic_method = "manhattan"

    # Initialize heuristic and set h, f for the start state
    start_state.h = compute_h(start_board, GOAL_STATE, heuristic_method)
    start_state.f = start_state.g + start_state.h

    print(f"\n🔎 Solving with A* using the {heuristic_method} heuristic...")

    # Time the search
    start_time = time.time()
    solution_path, expanded_nodes = a_star_search(start_state, GOAL_STATE, heuristic_method)
    end_time = time.time()

    if solution_path:
        print(f"\n✅ Puzzle solved in {len(solution_path)-1} moves!")
        print(f"⏱️  Time taken: {end_time - start_time:.4f} seconds")
        print(f"📚 Nodes expanded: {expanded_nodes}")
        print("\n🧩 Solution Path:")
        for step, state in enumerate(solution_path):
            print(f"\nStep {step}:")
            print(state)
    else:
        print("\n❌ No solution found.")

if __name__ == "__main__":
    main()
