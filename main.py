# main.py

import os
from puzzles.config import GOAL_STATE
from puzzles.helpers import generate_random_board
from puzzles.heuristics import hamming_distance, manhattan_distance, compute_h
from puzzles.puzzle import PuzzleState, open_file


def main():
    # Optional: Open GIF if it exists
    gif_path = os.path.join("experiments", "giphy.webp")
    if os.path.exists(gif_path):
        print("\n🎬 Opening GIF for fun...")
        open_file(gif_path)
    else:
        print("\n(No GIF found. Put 'giphy.webp' in 'experiments/' to auto-open.)")

    # Generate a random solvable board
    start_board = generate_random_board()
    start_state = PuzzleState(start_board)

    print("\n🧩 Start State:")
    print(start_state)

    # Compute heuristic values
    h_hamming = hamming_distance(start_board, GOAL_STATE)
    h_manhattan = manhattan_distance(start_board, GOAL_STATE)

    print("\n📊 Heuristic Values:")
    print(f"Hamming Distance: {h_hamming}")
    print(f"Manhattan Distance: {h_manhattan}")

    # Compute using selector function
    print("\n🔍 compute_h() selector test:")
    print(f"compute_h(..., 'hamming') = {compute_h(start_board, GOAL_STATE, 'hamming')}")
    print(f"compute_h(..., 'manhattan') = {compute_h(start_board, GOAL_STATE, 'manhattan')}")

    # Show neighbors
    print("\n🔄 Neighbor States:")
    neighbors = start_state.neighbors()
    print(f"Total neighbors: {len(neighbors)}")
    for i, neighbor in enumerate(neighbors, 1):
        print(f"\nNeighbor {i} (g={neighbor.g}, h={neighbor.h}, f={neighbor.f}):")
        print(neighbor)


if __name__ == "__main__":
    main()