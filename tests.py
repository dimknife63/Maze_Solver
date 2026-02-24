import unittest
from mac_demo import Maze  # or `from maze import Maze` if saved as maze.py

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._Maze__cells), num_cols)
        self.assertEqual(len(m1._Maze__cells[0]), num_rows)

    def test_maze_different_sizes(self):
        # Small maze
        m2 = Maze(0, 0, 2, 3, 5, 5)
        self.assertEqual(len(m2._Maze__cells), 3)
        self.assertEqual(len(m2._Maze__cells[0]), 2)

        # Larger maze
        m3 = Maze(0, 0, 20, 30, 15, 15)
        self.assertEqual(len(m3._Maze__cells), 30)
        self.assertEqual(len(m3._Maze__cells[0]), 20)

if __name__ == "__main__":
    unittest.main()