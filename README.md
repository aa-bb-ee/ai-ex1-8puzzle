# ai-ex1-8puzzle
AI Exercise 1, 8-Puzzle Solver (Heuristic Search)


This project implements the 8-Puzzle problem using the A* search algorithm
and compares two heuristics:

**Hamming Distance** → number of misplaced tiles

**Manhattan Distance** → sum of distances of tiles from their goal positions

The goal is to evaluate both heuristics in terms of memory usage (expanded nodes) and computation time.


1. **Project Structure**

<pre>
AI_Task1/
│
├── puzzles/               # Core puzzle logic
│   ├── puzzle.py          # State, neighbors, solvability check
│   ├── heuristics.py      # Hamming and Manhattan heuristics
│   └── search.py          # A* algorithm
│
├── experiments/           # Benchmark and performance comparison
│   └── benchmark.py
│
├── tests/                 # Unit tests (pytest)
│   ├── test_puzzle.py
│   ├── test_search.py
│   └── test_heuristics.py
│
├── main.py                # Entry point
├── requirements.txt       # Dependencies
└── README.md              # Documentation
</pre>

