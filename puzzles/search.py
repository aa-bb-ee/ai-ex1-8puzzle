import heapq

from puzzles.heuristics import compute_h


def a_star_search(start_state, goal_state, heuristic_method):
    """
    Perform A* search algorithm to solve the 8-Puzzle.

    Parameters:
    - start_state: PuzzleState object representing start configuration
    - goal_state: list representing the goal board configuration
    - heuristic_method: string name of heuristic ("hamming" or "manhattan")

    Returns:
    - path: list of PuzzleState objects, from start to goal (solution path)
    - explored_count: int, number of states expanded during search
    """

    # Priority queue for frontier, initialized with start state
    # Elements are tuples of (f, PuzzleState). heapq ensures lowest f is poped first
    frontier = []
    heapq.heappush(frontier, (start_state.f, start_state))

    # Explored set to keep track of visited states to avoid repeats
    explored = set()

    # For statistics: how many states have been expanded
    explored_count = 0

    while frontier:
        # Get the state with lowest f = g + h
        current_f, current_state = heapq.heappop(frontier)

        # Check if goal reached
        if current_state.board == goal_state:
            # Reconstruct the path by following parents (if you store them),
            # or just return current_state for now
            return reconstruct_path(current_state), explored_count

        # Mark current state as explored
        explored.add(current_state)

        # Expand neighbors (possible moves)
        for neighbor in current_state.neighbors():
            if neighbor in explored:
                continue

            # Calculate heuristic h for neighbor
            neighbor.h = compute_h(neighbor.board, goal_state, heuristic_method)

            # g = cost so far (moves from start), increase by 1 per step
            neighbor.g = current_state.g + 1

            # f = g + h
            neighbor.f = neighbor.g + neighbor.h

            # Store parent to reconstruct path later
            neighbor.parent = current_state

            # Add neighbor to frontier for further exploration
            heapq.heappush(frontier, (neighbor.f, neighbor))

        explored_count += 1

    # If no solution found
    return None, explored_count

def reconstruct_path(state):
    """Helper function to reconstruct the solution path from goal to start."""
    path = []
    while state:
        path.append(state)
        state = getattr(state, 'parent', None)
    path.reverse()
    return path
