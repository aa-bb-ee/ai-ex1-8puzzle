import os, sys, subprocess

def open_file(path: str):
    """Open a file with the default app (works for .gif, .webp, .png, etc.)."""
    if sys.platform.startswith("darwin"):
        subprocess.Popen(["open", path])          # macOS
    elif os.name == "nt":
        os.startfile(path)                        # Windows
    else:
        subprocess.Popen(["xdg-open", path])

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
        row = [num_to_emoji[x] for x in board[i:i+3]]
        rows.append(' '.join(row))
    return '\n'.join(rows)

class PuzzleState:
    def __init__(self, board, g=0, h=0):
        self.board = board
        self.g = g
        self.h = h
        self.f = g + h
        self.blank_index = board.index(0)

    def neighbors(self):
        moves = []
        row, col = divmod(self.blank_index, 3)
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 3 and 0 <= c < 3:
                new_board = self.board[:]  # shallow copy is enough
                new_blank = r * 3 + c
                # swap blank with the neighbor tile
                new_board[self.blank_index], new_board[new_blank] = \
                    new_board[new_blank], new_board[self.blank_index]
                moves.append(PuzzleState(new_board, self.g + 1))
        return moves

    def __eq__(self, other):
        return tuple(self.board) == tuple(other.board)

    def __hash__(self):
        return hash(tuple(self.board))

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        """Pretty-print when you do print(state)."""
        return format_board(self.board)

    def pretty_print(self):
        """Optional explicit printer, if you prefer a method."""
        print(self.__str__())


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gif_path = os.path.join(BASE_DIR, "experiments", "giphy.webp")
    if os.path.exists(gif_path):
        print(f"\nSmall surprise - me doing this task:")
        open_file(gif_path)
    else:
        print(f"\n(No GIF found at {gif_path}. Put your file there to auto-open.)")


    # quick demo: generate neighbors from a simple state
    s = PuzzleState([1, 2, 3,
                     4, 0, 5,
                     6, 7, 8])  # blank in the center

    print("Start state:")
    print(s)  # uses __str__ -> nice 3x3 grid

    ns = s.neighbors()
    print("\nNumber of neighbors:", len(ns))

    for i, n in enumerate(ns, 1):
        print(f"\nNeighbor {i} (g={n.g}, h={n.h}, f={n.f}):")
        print(n)  # also prints as a grid
