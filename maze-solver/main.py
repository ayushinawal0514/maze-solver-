"""
Maze Generator & Solver
------------------------
Generates a random maze with a stack-based DFS backtracker, then races
BFS (queue) against A* (priority queue) to solve it, visualized in pygame.

Usage:
    python main.py
    python main.py --width 40 --height 25 --seed 42
"""
import argparse
from maze import Maze
from solvers import bfs_solve, astar_solve
from visualizer import MazeVisualizer


def main():
    parser = argparse.ArgumentParser(description="Maze Generator & Solver (DFS build, BFS vs A* race)")
    parser.add_argument("--width", type=int, default=30, help="maze width in cells (default: 30)")
    parser.add_argument("--height", type=int, default=20, help="maze height in cells (default: 20)")
    parser.add_argument("--seed", type=int, default=None, help="random seed for a reproducible maze")
    args = parser.parse_args()

    maze = Maze(args.width, args.height, seed=args.seed)
    viz = MazeVisualizer(maze)

    # Phase 1: carve the maze with a stack-based DFS backtracker
    viz.animate_generation(maze.generate())

    # Phase 2: race BFS (queue) vs A* (priority queue) top-left -> bottom-right
    start = maze.cell(0, 0)
    goal = maze.cell(maze.width - 1, maze.height - 1)
    viz.race_solvers(bfs_solve(maze, start, goal), astar_solve(maze, start, goal), start, goal)

    viz.wait_for_close()


if __name__ == "__main__":
    main()
