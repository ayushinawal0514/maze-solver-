"""
Pygame front-end. Draws the maze being carved out, then shows BFS and A*
solving it side by side so you can literally watch the difference between
"explore everything nearby" (queue) and "explore the promising stuff first"
(priority queue).
"""
import sys
import pygame

CELL_SIZE = 22
MARGIN = 20
PANEL_GAP = 60
FPS_GENERATE = 400
FPS_SOLVE = 120

COLOR_BG = (18, 18, 24)
COLOR_WALL = (230, 230, 240)
COLOR_VISITED_GEN = (60, 60, 90)
COLOR_STACK_TOP = (255, 180, 60)
COLOR_BFS_VISITED = (60, 140, 220)
COLOR_ASTAR_VISITED = (220, 90, 140)
COLOR_PATH = (80, 230, 140)
COLOR_START = (255, 220, 70)
COLOR_GOAL = (255, 90, 90)
COLOR_TEXT = (235, 235, 240)


class MazeVisualizer:
    def __init__(self, maze):
        self.maze = maze
        pygame.init()
        pygame.display.set_caption("Maze Generator & Solver — DFS build, BFS vs A* race")
        self.font = pygame.font.SysFont("consolas", 18)
        self.panel_w = maze.width * CELL_SIZE
        self.panel_h = maze.height * CELL_SIZE
        width = MARGIN * 2 + self.panel_w * 2 + PANEL_GAP
        height = MARGIN * 2 + self.panel_h + 60
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

    def _origin(self, panel_index):
        x = MARGIN + panel_index * (self.panel_w + PANEL_GAP)
        y = MARGIN + 40
        return x, y

    def _draw_cell_walls(self, panel_index, cell):
        ox, oy = self._origin(panel_index)
        x, y = ox + cell.x * CELL_SIZE, oy + cell.y * CELL_SIZE
        w = cell.walls
        if w["N"]:
            pygame.draw.line(self.screen, COLOR_WALL, (x, y), (x + CELL_SIZE, y), 2)
        if w["S"]:
            pygame.draw.line(self.screen, COLOR_WALL, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if w["E"]:
            pygame.draw.line(self.screen, COLOR_WALL, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if w["W"]:
            pygame.draw.line(self.screen, COLOR_WALL, (x, y), (x, y + CELL_SIZE), 2)

    def _fill_cell(self, panel_index, cell, color, pad=3):
        ox, oy = self._origin(panel_index)
        x, y = ox + cell.x * CELL_SIZE, oy + cell.y * CELL_SIZE
        rect = pygame.Rect(x + pad, y + pad, CELL_SIZE - pad * 2, CELL_SIZE - pad * 2)
        pygame.draw.rect(self.screen, color, rect, border_radius=3)

    def _draw_maze_walls(self, panel_index):
        for col in self.maze.grid:
            for cell in col:
                self._draw_cell_walls(panel_index, cell)

    def _draw_label(self, panel_index, text):
        ox, _ = self._origin(panel_index)
        surf = self.font.render(text, True, COLOR_TEXT)
        self.screen.blit(surf, (ox, MARGIN))

    def _pump(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

    def animate_generation(self, generator):
        """Phase 1: draw the DFS backtracker carving the maze, wall by wall."""
        self.screen.fill(COLOR_BG)
        self._draw_label(0, "Generating maze (stack-based DFS backtracker)")
        pygame.display.flip()

        path_stack = [self.maze.grid[0][0]]
        for event in generator:
            self._pump()
            if event[0] == "carve":
                path_stack.append(event[2])
            elif event[0] == "backtrack":
                if len(path_stack) > 1:
                    path_stack.pop()

            self.screen.fill(COLOR_BG, pygame.Rect(*self._origin(0), self.panel_w, self.panel_h))
            for cell in path_stack:
                self._fill_cell(0, cell, COLOR_VISITED_GEN)
            self._fill_cell(0, path_stack[-1], COLOR_STACK_TOP)
            self._draw_maze_walls(0)
            pygame.display.flip()
            self.clock.tick(FPS_GENERATE)

        pygame.time.wait(400)

    def race_solvers(self, bfs_gen, astar_gen, start, goal):
        """Phase 2: run BFS and A* in lock-step, one panel each, and compare."""
        self.screen.fill(COLOR_BG)
        pygame.display.flip()

        bfs_visited, astar_visited = [], []
        bfs_path, astar_path = [], []
        bfs_done = astar_done = False
        bfs_count = astar_count = 0

        while not (bfs_done and astar_done):
            self._pump()
            if not bfs_done:
                try:
                    kind, payload = next(bfs_gen)
                    if kind == "visit":
                        bfs_visited.append(payload)
                        bfs_count += 1
                    else:
                        bfs_path = payload
                        bfs_done = True
                except StopIteration:
                    bfs_done = True
            if not astar_done:
                try:
                    kind, payload = next(astar_gen)
                    if kind == "visit":
                        astar_visited.append(payload)
                        astar_count += 1
                    else:
                        astar_path = payload
                        astar_done = True
                except StopIteration:
                    astar_done = True

            for panel, visited, path, color in (
                (0, bfs_visited, bfs_path, COLOR_BFS_VISITED),
                (1, astar_visited, astar_path, COLOR_ASTAR_VISITED),
            ):
                self.screen.fill(COLOR_BG, pygame.Rect(*self._origin(panel), self.panel_w, self.panel_h))
                for cell in visited:
                    self._fill_cell(panel, cell, color)
                for cell in path:
                    self._fill_cell(panel, cell, COLOR_PATH)
                self._fill_cell(panel, start, COLOR_START)
                self._fill_cell(panel, goal, COLOR_GOAL)
                self._draw_maze_walls(panel)

            self._draw_label(0, f"BFS  (queue)      visited: {bfs_count}")
            self._draw_label(1, f"A*   (heap)       visited: {astar_count}")
            pygame.display.flip()
            self.clock.tick(FPS_SOLVE)

        if bfs_count < astar_count:
            winner = "BFS explored fewer cells"
        elif astar_count < bfs_count:
            winner = "A* explored fewer cells"
        else:
            winner = "Tie"
        summary = f"BFS visited {bfs_count} cells  |  A* visited {astar_count} cells  |  {winner}  |  (Esc to quit)"
        surf = self.font.render(summary, True, COLOR_TEXT)
        self.screen.blit(surf, (MARGIN, self.screen.get_height() - 30))
        pygame.display.flip()

    def wait_for_close(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
            self.clock.tick(30)
