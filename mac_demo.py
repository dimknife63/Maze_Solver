import time
import random
from tkinter import Tk, BOTH, Canvas

# --- Point and Line classes ---
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start_point, end_point):
        self.start = start_point
        self.end = end_point

    def draw(self, canvas, fill_color="black"):
        if canvas is not None:
            canvas.create_line(
                self.start.x, self.start.y,
                self.end.x, self.end.y,
                fill=fill_color,
                width=2
            )

# --- Window class ---
class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze")
        self.__root.geometry(f"{width}x{height}")
        self.canvas = Canvas(self.__root, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)

# --- Cell class ---
class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False

        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1

        self.__win = win

    def draw(self, x1, y1, x2, y2):
        self.__x1, self.__y1 = x1, y1
        self.__x2, self.__y2 = x2, y2

        if self.__win is None:
            return

        bg_color = "#d9d9d9"  # background color

        # Draw each wall (black if exists, background color if removed)
        color = "black" if self.has_left_wall else bg_color
        self.__win.draw_line(Line(Point(x1, y1), Point(x1, y2)), fill_color=color)

        color = "black" if self.has_right_wall else bg_color
        self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), fill_color=color)

        color = "black" if self.has_top_wall else bg_color
        self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), fill_color=color)

        color = "black" if self.has_bottom_wall else bg_color
        self.__win.draw_line(Line(Point(x1, y2), Point(x2, y2)), fill_color=color)

    def draw_move(self, to_cell, undo=False):
        if self.__win is None:
            return
        x1 = (self.__x1 + self.__x2) / 2
        y1 = (self.__y1 + self.__y2) / 2
        x2 = (to_cell.__x1 + to_cell.__x2) / 2
        y2 = (to_cell.__y1 + to_cell.__y2) / 2
        color = "gray" if undo else "red"
        self.__win.draw_line(Line(Point(x1, y1), Point(x2, y2)), fill_color=color)

# --- Maze class ---
class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []

        if seed is not None:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__generate_maze()          # recursive DFS
        self.__reset_cells_visited()    # reset for solving

    def __create_cells(self):
        for i in range(self.num_cols):
            column = []
            for j in range(self.num_rows):
                column.append(Cell(self.__win))
            self.__cells.append(column)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        x_start = self.x1 + i * self.cell_size_x
        y_start = self.y1 + j * self.cell_size_y
        x_end = x_start + self.cell_size_x
        y_end = y_start + self.cell_size_y

        self.__cells[i][j].draw(x_start, y_start, x_end, y_end)
        self.__animate()

    def __animate(self):
        if self.__win is not None:
            self.__win.redraw()
            time.sleep(0.05)

    def __break_entrance_and_exit(self):
        if not self.__cells:
            return
        # Entrance
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        # Exit
        self.__cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.num_cols - 1, self.num_rows - 1)

    def __generate_maze(self):
        self.__break_walls_r(0, 0)

    def __break_walls_r(self, i, j):
        current = self.__cells[i][j]
        current.visited = True

        while True:
            directions = []

            if i > 0 and not self.__cells[i-1][j].visited:
                directions.append(("left", i-1, j))
            if i < self.num_cols - 1 and not self.__cells[i+1][j].visited:
                directions.append(("right", i+1, j))
            if j > 0 and not self.__cells[i][j-1].visited:
                directions.append(("up", i, j-1))
            if j < self.num_rows - 1 and not self.__cells[i][j+1].visited:
                directions.append(("down", i, j+1))

            if not directions:
                self.__draw_cell(i, j)
                return

            direction, ni, nj = random.choice(directions)
            neighbor = self.__cells[ni][nj]

            # Remove walls between current and neighbor
            if direction == "left":
                current.has_left_wall = False
                neighbor.has_right_wall = False
            elif direction == "right":
                current.has_right_wall = False
                neighbor.has_left_wall = False
            elif direction == "up":
                current.has_top_wall = False
                neighbor.has_bottom_wall = False
            elif direction == "down":
                current.has_bottom_wall = False
                neighbor.has_top_wall = False

            self.__draw_cell(i, j)
            self.__break_walls_r(ni, nj)

    def __reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__cells[i][j].visited = False

    # --- Maze solving ---
    def solve(self):
        self.__reset_cells_visited()
        return self.__solve_r(0, 0)

    def __solve_r(self, i, j):
        self.__animate()
        current = self.__cells[i][j]
        current.visited = True

        # End cell
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        neighbors = []
        if not current.has_left_wall and i > 0 and not self.__cells[i-1][j].visited:
            neighbors.append((i-1, j))
        if not current.has_right_wall and i < self.num_cols - 1 and not self.__cells[i+1][j].visited:
            neighbors.append((i+1, j))
        if not current.has_top_wall and j > 0 and not self.__cells[i][j-1].visited:
            neighbors.append((i, j-1))
        if not current.has_bottom_wall and j < self.num_rows - 1 and not self.__cells[i][j+1].visited:
            neighbors.append((i, j+1))

        for ni, nj in neighbors:
            neighbor = self.__cells[ni][nj]
            current.draw_move(neighbor)  # forward path
            if self.__solve_r(ni, nj):
                return True
            else:
                current.draw_move(neighbor, undo=True)  # backtrack

        return False

# --- Demo ---
if __name__ == "__main__":
    win = Window(800, 600)
    maze = Maze(50, 50, 10, 15, 40, 40, win, seed=0)  # 10 rows x 15 cols
    maze.solve()  # animate the solution
    win.wait_for_close()