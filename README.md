# AI Exercise 1 – 8-Puzzle Solver (Heuristic Search)

This project implements the 8-Puzzle problem using the A* search algorithm and compares two heuristic functions:

- **Hamming Distance** – number of misplaced tiles  
- **Manhattan Distance** – sum of distances of tiles from their goal positions  

The goal is to evaluate both heuristics in terms of **memory usage** (expanded nodes) and **computation time**.

---


## Project Structure

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



---

## Setup Instructions (macOS & Windows)

### 1. Clone the Repository

<pre>
git clone https://github.com/aa-bb-ee/ai-ex1-8puzzle.git
cd ai-ex1-8puzzle        # in the terminal (PyCharm > View > Tool Windows > Terminal)
</pre>

### 2. Create a Virtual Environment

**macOS / Linux**
<pre>
python3 -m venv venv
source venv/bin/activate
</pre>

**Windows (PowerShell)**
<pre>
python -m venv venv
venv\Scripts\activate
</pre>

**Git Bash**

<pre>
python3 -m venv venv
source venv/Scripts/activate
</pre>

If successful, your terminal will show:
<pre> 
(venv) ... 
</pre>


---

### 3. Install Dependencies

<pre>
pip install --upgrade pip
pip install -r requirements.txt
</pre>

If `requirements.txt` is empty or missing, install manually:
<pre>
pip install pandas pytest
</pre>

---

### 4. (Optional) Save New Dependencies

If you install new packages later:
<pre>
pip freeze > requirements.txt
</pre>

---

## Running the Project

**Via Terminal**
<pre>
python main.py
</pre>

**Via PyCharm**
1. Open `main.py`
2. Click "Run main"

The script will:
- Generate random start states  
- Check solvability  
- Solve using A* with two heuristics  
- Measure expanded nodes and execution time

---

## Running Tests

<pre>
pytest -v
</pre>

This runs all tests from the `tests/` directory and displays pass/fail results.

---

## Benchmark Experiments

File: `experiments/benchmark.py`

This module:
- Runs 100 random solvable states  
- Compares Hamming vs. Manhattan heuristics  
- Measures:
  - Average nodes expanded  
  - Mean execution time  
  - Standard deviation for both

Results can be saved to a CSV file (e.g., `results_8puzzle.csv`).

---

## Team Collaboration

### Team Workflow
Each team member should:

<pre>
git clone https://github.com/aa-bb-ee/ai-ex1-8puzzle.git
cd ai-ex1-8puzzle
</pre>

MacOS/Linux
<pre>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
</pre>

Windows
<pre>
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
</pre>


Then create a new branch for their task:

<pre>
git checkout -b feature/add-manhattan-heuristic
</pre>

After finishing:

<pre>
git add .
git commit -m "Implement Manhattan heuristic"
git push -u origin feature/add-manhattan-heuristic
</pre>

Finally, open a Pull Request on GitHub for review.

![8-Puzzle Demo](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmw4ZXJhYTdkNDd2bDhteDcwdnVpcjB3cGt2djc4YTlqM3o4OHd1OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/k2Da0Uzaxo9xe/giphy.gif)
