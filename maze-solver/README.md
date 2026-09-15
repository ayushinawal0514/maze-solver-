# Maze Generator & Solver — DFS Build, BFS vs A* Race

A visual playground for graph algorithms and the data structures behind them.
It generates a random maze, then races two pathfinding algorithms against
each other so you can literally watch a queue-based search versus a
priority-queue-based search explore the same space.

![status](https://img.shields.io/badge/status-working-brightgreen)
![python](https://img.shields.io/badge/python-3.9%2B-blue)

## What it does

1. **Generates** a maze using an iterative DFS "recursive backtracker,"
   driven by an explicit **stack** — you can watch it carve the maze in
   real time.
2. **Solves** the maze two ways, side by side:
   - **BFS**, using a **queue** (`collections.deque`) — explores level by
     level, guaranteed shortest path.
   - **A\***, using a **priority queue / binary heap** (`heapq`) — uses a
     distance heuristic to explore promising cells first, usually visiting
     far fewer cells for the same shortest path.
3. Displays a live visited-cell counter for both algorithms and declares
   which one explored fewer cells.

## Data structures in play

| Structure          | Where it's used                              |
|---------------------|-----------------------------------------------|
| Stack               | Maze generation (DFS backtracker)             |
| Graph (implicit)     | The maze itself — cells are nodes, open walls are edges |
| Queue                | BFS solver                                    |
| Priority queue / heap | A* solver                                    |
| Hash sets/maps       | Visited tracking, `came_from` path reconstruction |

## Requirements

- Python 3.9+
- `pygame`

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/maze-solver.git
cd maze-solver
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Optional flags:

```bash
python main.py --width 40 --height 25 --seed 42
```

- `--width`, `--height` — maze size in cells (default 30x20)
- `--seed` — fix the random seed for a reproducible maze

Press **Esc** or close the window to quit at any point.

## Project structure

```
maze-solver/
├── main.py         # entry point — wires generation, solving, visualization together
├── maze.py          # Maze + Cell classes, stack-based DFS generation
├── solvers.py       # bfs_solve() and astar_solve(), written as generators
├── visualizer.py     # all pygame drawing and animation logic
├── requirements.txt
└── README.md
```

## How the algorithms are implemented

Both solvers are Python **generators** — they `yield` a `("visit", cell)`
event every time they pop a cell, and finish with `("done", path)`. This is
what lets `visualizer.py` step them forward one frame at a time and run them
concurrently for the race, instead of running each one to completion first.

- `bfs_solve`: a plain `deque` used strictly as a FIFO queue — append to the
  right, pop from the left.
- `astar_solve`: a `heapq` min-heap keyed on `cost_so_far + heuristic`, with
  Manhattan distance as the heuristic and a tie-breaking counter so the heap
  never has to compare `Cell` objects directly.

## Ideas to extend it

- Add Dijkstra's algorithm as a third racer (A* without the heuristic)
- Add diagonal movement
- Support loading/saving mazes to a file
- Add a "weighted terrain" mode (some cells cost more to enter) to show off
  A*'s advantage over BFS more dramatically
- Swap the animation loop for `asyncio` and run the race in true parallel time

## License

MIT — do whatever you want with it.
