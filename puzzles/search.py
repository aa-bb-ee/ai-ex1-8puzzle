import heapq
import itertools
from puzzles.heuristics import compute_h


def a_star_search(start_state, goal_state, heuristic_method):
    """
    Perform A* search algorithm to solve the 8-Puzzle.

    Tie-breaking priority:
      1. Lower f = g + h
      2. Lower h (closer to goal)
      3. Earlier insertion (FIFO)

    Parameters:
    - start_state: PuzzleState object representing start configuration
    - goal_state: list representing the goal board configuration
    - heuristic_method: string name of heuristic ("hamming" or "manhattan")

    Returns:
    - path: list of PuzzleState objects, from start to goal (solution path)
    - explored_count: int, number of states expanded during search
    """

    # ---
    # Initialization
    # ---
    counter = itertools.count()  # unique incremental tie-break counter
    frontier = []  # heap-based priority queue
    explored = set()  # to avoid revisiting states

    # Initialize start state's heuristic values
    start_state.h = compute_h(start_state.board, goal_state, heuristic_method)
    start_state.f = start_state.g + start_state.h

    # Push start node into frontier with tie-breaking tuple
    heapq.heappush(frontier, (start_state.f, start_state.h, next(counter), start_state))
    explored_count = 0

    # ---
    # A* Main Loop
    # ---
    while frontier:
        # Pop node with lowest (f, h, order)
        _, _, _, current_state = heapq.heappop(frontier)

        # Goal test
        if current_state.board == goal_state:
            return reconstruct_path(current_state), explored_count

        # Skip if already expanded
        if current_state in explored:
            continue
        explored.add(current_state)

        explored_count += 1

        # Expand neighbors (possible moves)
        for neighbor in current_state.neighbors():
            if neighbor in explored:
                continue

            # Compute heuristic, g, f
            neighbor.h = compute_h(neighbor.board, goal_state, heuristic_method)
            neighbor.g = current_state.g + 1
            neighbor.f = neighbor.g + neighbor.h
            neighbor.parent = current_state

            # Push with deterministic tie-breaking
            heapq.heappush(frontier, (neighbor.f, neighbor.h, next(counter), neighbor))

    # If frontier empty and no goal found
    return None, explored_count


def reconstruct_path(state):
    """Reconstruct the solution path by following parent links."""
    path = []
    while state:
        path.append(state)
        state = getattr(state, 'parent', None)
    path.reverse()
    return path
