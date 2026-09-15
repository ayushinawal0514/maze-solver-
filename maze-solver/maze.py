"""
Maze representation and generation.

The maze is carved out of a grid using a *recursive backtracker*, implemented
iteratively with an explicit STACK (a core data structure) instead of
function-call recursion. That's the classic DFS maze-generation algorithm.
"""
import random


class Cell:
    """A single cell in the maze grid. Walls start up on all four sides."""

    __slots__ = ("x", "y", "walls", "visited")

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"N": True, "S": True, "E": True, "W": True}
        self.visited = False

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"


class Maze:
    DX = {"N": 0, "S": 0, "E": 1, "W": -1}
    DY = {"N": -1, "S": 1, "E": 0, "W": 0}
    OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}

    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        if seed is not None:
            random.seed(seed)

    def cell(self, x, y):
        return self.grid[x][y]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def _neighbors(self, cell):
        for direction in ("N", "S", "E", "W"):
            nx, ny = cell.x + self.DX[direction], cell.y + self.DY[direction]
            if self.in_bounds(nx, ny):
                yield direction, self.grid[nx][ny]

    def unvisited_neighbors(self, cell):
        return [(d, n) for d, n in self._neighbors(cell) if not n.visited]

    def accessible_neighbors(self, cell):
        """Neighbors reachable from `cell` (no wall between them). Used by solvers."""
        return [n for direction, n in self._neighbors(cell) if not cell.walls[direction]]

    def remove_wall(self, a, b):
        for direction in ("N", "S", "E", "W"):
            if a.x + self.DX[direction] == b.x and a.y + self.DY[direction] == b.y:
                a.walls[direction] = False
                b.walls[self.OPPOSITE[direction]] = False
                return

    def generate(self):
        """
        Iterative DFS backtracker using an EXPLICIT STACK.

        Yields animation events so the visualizer can draw each step:
          ("carve", current_cell, new_cell)  -> a wall was knocked down
          ("backtrack", cell)                -> we popped back to this cell
        """
        start = self.grid[0][0]
        start.visited = True
        stack = [start]  # <-- the stack that drives the whole algorithm

        while stack:
            current = stack[-1]
            neighbors = self.unvisited_neighbors(current)
            if neighbors:
                direction, next_cell = random.choice(neighbors)
                self.remove_wall(current, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
                yield ("carve", current, next_cell)
            else:
                stack.pop()
                if stack:
                    yield ("backtrack", stack[-1])
