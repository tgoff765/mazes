import unittest
from maze_creator.grids.grid import Grid


class TestGrids(unittest.TestCase):
    def test_grid_setup(self):
        test_grid = Grid(2, 2)

        expected = 2
        self.assertEqual(test_grid.columns, expected)
        self.assertEqual(test_grid.columns, expected)

    def test_grid_size(self):
        test_grid = Grid(2, 5)

        expected = 10
        self.assertEqual(test_grid.size(), expected)
