"""
Two maze solvers, written as generators so the visualizer can animate them
one step at a time and race them side by side.

  bfs_solve()   -> uses a QUEUE (collections.deque)
  astar_solve() -> uses a PRIORITY QUEUE / binary heap (heapq)
"""
from collections import deque
import heapq


def _reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return []
    path = [goal]
    while path[-1] is not start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def bfs_solve(maze, start, goal):
    """
    Breadth-first search. Guaranteed shortest path in an unweighted maze.
    Yields ("visit", cell) for every cell popped off the queue, then
    finally yields ("done", path).
    """
    queue = deque([start])          # the queue
    came_from = {start: None}
    seen = {start}

    while queue:
        current = queue.popleft()
        yield ("visit", current)
        if current is goal:
            break
        for neighbor in maze.accessible_neighbors(current):
            if neighbor not in seen:
                seen.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    yield ("done", _reconstruct_path(came_from, start, goal))


def astar_solve(maze, start, goal):
    """
    A* search: BFS's cousin that uses a heuristic (Manhattan distance) to
    explore promising cells first, via a PRIORITY QUEUE (heapq / binary heap).
    Also finds the shortest path, usually visiting far fewer cells than BFS.
    """
    def heuristic(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    counter = 0  # tie-breaker so heapq never has to compare Cell objects
    frontier = [(0, counter, start)]   # the priority queue (min-heap)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, _, current = heapq.heappop(frontier)
        yield ("visit", current)
        if current is goal:
            break
        for neighbor in maze.accessible_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                counter += 1
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, counter, neighbor))
                came_from[neighbor] = current

    yield ("done", _reconstruct_path(came_from, start, goal))
