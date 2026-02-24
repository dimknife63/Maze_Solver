# Maze Generator & Solver

This is a Python program that generates a random maze and visually solves it using depth-first search (DFS). The project uses **Tkinter** for graphical display, showing both the maze creation process and the solving path with animations.

---

## Features

- Animated maze generation using depth-first search
- Entrance (top-left) and exit (bottom-right) removed
- Each maze is randomly generated, with optional **seed** for reproducibility
- DFS-based maze solver with red path and gray backtracking
- Cells can be reused for solving after generation (visited flags reset)
- Adjustable maze size and cell dimensions

---

## Requirements

- Python 3.x
- Tkinter (usually included with Python)

---

## How to Run

1. Open a terminal in the project folder
2. Run the maze generator and solver:

```bash
python3 mac_demo.py