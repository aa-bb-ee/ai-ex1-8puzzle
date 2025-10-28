
def format_board(board):
    """Return a nicely formatted 3x3 board as a string with emojis (0 shown as blank circle)."""
    num_to_emoji = {
        0: '⚫',
        1: '1️⃣',
        2: '2️⃣',
        3: '3️⃣',
        4: '4️⃣',
        5: '5️⃣',
        6: '6️⃣',
        7: '7️⃣',
        8: '8️⃣',
    }
    rows = []
    for i in range(0, 9, 3):
        # Map each tile in the row to its emoji and join with spaces
        row = [num_to_emoji[x] for x in board[i:i+3]]
        rows.append(' '.join(row))
    return '\n'.join(rows)

class PuzzleState:
    """
    Minimal 8-puzzle state container.

    Attributes:
      - board: list[int] length 9, 0..8 with 0 as blank.
      - g: path cost from the start (number of moves so far).
      - h: heuristic estimate to the goal (set by the search algorithm).
      - f: total score used by A* (f = g + h).
      - blank_index: cached index of the blank to speed up neighbor generation.
    """

    def __init__(self, board, g=0, h=0):
        self.board = board
        self.g = g
        self.h = h
        self.f = g + h
        self.blank_index = board.index(0)  # cache blank position

    def neighbors(self):
        """
        Generate all states reachable by sliding one tile into the blank.
        Only up/down/left/right moves within the 3×3 grid are allowed.
        """
        moves = []
        row, col = divmod(self.blank_index, 3)

        # 4-way movement deltas: up, down, left, right
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 3 and 0 <= c < 3:
                new_board = self.board[:]  # shallow copy is enough
                new_blank = r * 3 + c

                # swap blank with the neighbor tile
                new_board[self.blank_index], new_board[new_blank] = \
                    new_board[new_blank], new_board[self.blank_index]

                # Create a child state with g+1; h will be set by the search
                moves.append(PuzzleState(new_board, self.g + 1))
        return moves

    # Equality/hash make states usable in sets/dicts (e.g., closed sets in A*)
    def __eq__(self, other):
        return tuple(self.board) == tuple(other.board)

    def __hash__(self):
        return hash(tuple(self.board))

    # __lt__ lets heapq/PriorityQueue break ties using f (useful for A*)
    # not used anymore in more advanced A* tie-break mode
    # def __lt__(self, other):
    #    return self.f < other.


    def __str__(self):
        """Pretty-print when you do print(state)."""
        return format_board(self.board)

    def pretty_print(self):
        """Optional explicit printer, if you prefer a method."""
        print(self.__str__())

# -------------------------------
# Demo (kept outside the class)
# -------------------------------
if __name__ == "__main__":
    # Start with the blank (0) in the center
    s = PuzzleState([
        1, 2, 3,
        4, 0, 5,
        6, 7, 8
    ])

    print("Start state:")
    print(s)  # uses __str__: shows a 3×3 grid

    ns = s.neighbors()
    print("\nNumber of neighbors:", len(ns))

    for i, n in enumerate(ns, 1):
        # h defaults to 0 here; A* would set it before pushing to the frontier
        print(f"\nNeighbor {i} (g={n.g}, h={n.h}, f={n.f}):")
        print(n)